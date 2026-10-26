from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    String
)

from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )


class LoginSession(Base):
    __tablename__ = "login_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    token_hash: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True,
        nullable=False
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False
    )


class ModuleParticlesProblems(Base):
    __tablename__ = "module_particle_problems"

    id: Mapped[int] = mapped_column(primary_key=True)

    difficulty: Mapped[int] = mapped_column(default=1)

    sentence_before: Mapped[str] = mapped_column(String(255))
    sentence_after: Mapped[str] = mapped_column(String(255))

    correct_answer: Mapped[str] = mapped_column(String(50))
    wrong_answers: Mapped[list[str]] = mapped_column(JSON)

    explanation: Mapped[str] = mapped_column(
        String(1000),
        nullable=True
    )