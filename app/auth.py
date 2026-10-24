from datetime import datetime, timedelta, timezone
from typing import Annotated
import os

from fastapi import (
    APIRouter,
    Cookie,
    Depends,
    HTTPException,
    Response,
    status,
)

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.concurrency import run_in_threadpool

from .database import get_db
from .models import User, LoginSession
from .schemas import (
    UserCreate,
    UserLogin,
    UserPublic
)
from .security import (
    hash_password,
    verify_password,
    generate_session_token,
    hash_session_token
)

router = APIRouter(prefix="/auth", tags=["Authentication"])

DBSession = Annotated[AsyncSession, Depends(get_db)]

COOKIE_NAME = "session_token"
SESSION_LIFETIME = timedelta(days=7)

IS_PRODUCTION = os.getenv("APP_ENV") == "production"


async def get_current_user(
        db: DBSession,
        session_token: Annotated[str | None, Cookie()] = None,
) -> User:
    if session_token is None:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    token_hash = hash_session_token(session_token)

    statement = select(LoginSession).where(
        LoginSession.token_hash == token_hash
    )
    result = await db.execute(statement)
    login_session = result.scalar_one_or_none()

    if login_session is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid session"
        )

    now = datetime.now(timezone.utc).replace(tzinfo=None)

    if (login_session.expires_at <= now):
        await db.delete(login_session)
        await db.commit()

        raise HTTPException(
            status_code=401,
            detail="Session expired"
        )

    user = await db.get(
        User,
        login_session.user_id,
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detial="User not found"
        )

    return user


@router.post(
    "/register",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
)
async def register(data: UserCreate, db: DBSession):
    statement = select(User).where(
        User.username == data.username
    )

    result = await db.execute(statement)
    existing_user = result.scalar_one_or_none()

    if existing_user is not None:
        raise HTTPException(
            status_code=400,
            detail="Username already taken"
        )

    hashed = await run_in_threadpool(
        hash_password,
        data.password
    )

    new_user = User(
        username = data.username,
        hashed_password = hashed
    )

    db.add(new_user)

    await db.commit()
    await db.refresh(new_user)

    return new_user



@router.post("/login")
async def login(
    data: UserLogin,
    response: Response,
    db: DBSession
):
    statement = select(User).where(
        User.username == data.username
    )
    result = await db.execute(statement)
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    password_valid = await run_in_threadpool(
        verify_password,
        data.password,
        user.hashed_password
    )

    if not password_valid:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )


    token = generate_session_token()
    expires_at = (
        datetime.now(timezone.utc).replace(tzinfo=None)
        + SESSION_LIFETIME
    )

    login_session = LoginSession(
        user_id = user.id,
        token_hash = hash_session_token(token),
        expires_at = expires_at
    )

    db.add(login_session)
    await db.commit()

    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        httponly=True,
        secure=IS_PRODUCTION,
        samesite="lax",
        max_age=int(SESSION_LIFETIME.total_seconds()),
        path="/"
    )

    return {"message" : "Login successful"}


@router.post("/logout")
async def logout(
    response: Response,
    db: DBSession,
    session_token: Annotated[str | None, Cookie()] = None
):
    if session_token is not None:
        token_hash = hash_session_token(session_token)

        statement = delete(LoginSession).where(
            LoginSession.token_hash == token_hash
        )

        await db.execute(statement)
        await db.commit()

    response.delete_cookie(
        key=COOKIE_NAME,
        path="/",
    )

    return {"message" : "Logged out successfully"}


CurrentUser = Annotated[User, Depends(get_current_user)]
@router.get(
    "/me",
    response_model=UserPublic
)
async def get_me(current_user: CurrentUser):
    return current_user