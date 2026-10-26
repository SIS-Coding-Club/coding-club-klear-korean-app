from datetime import datetime, timedelta, timezone
from typing import Annotated
import os
import random

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status,
)

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.concurrency import run_in_threadpool

from .database import get_db
from .models import ModuleParticlesProblems, User
from .schemas import (
    ModuleParticleCreate,
    ModuleParticlePublic
)
from .auth import get_current_user

router = APIRouter(prefix="/module-particle", tags=["ModuleParticle"])


DBSession = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post(
    "/create-problem",
    response_model=ModuleParticlePublic,
    status_code=status.HTTP_201_CREATED
)
async def create_problem(problem: ModuleParticleCreate, current_user: CurrentUser, db: DBSession):
    new_problem = ModuleParticlesProblems(**problem.model_dump())

    db.add(new_problem)

    await db.commit()
    await db.refresh(new_problem)

    possible_answers = [new_problem.correct_answer, *new_problem.wrong_answers]

    random.shuffle(possible_answers)

    return_problem = ModuleParticlePublic(
        id = new_problem.id,
        difficulty = new_problem.difficulty,
        sentence_before = new_problem.sentence_before,
        sentence_after = new_problem.sentence_after,
        possible_answers = possible_answers,
    )

    return return_problem