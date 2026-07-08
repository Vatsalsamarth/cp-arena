from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Index, Integer, Text, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.problem import Problem
    from app.models.user import User


class SubmissionStatus(str, Enum):
    """
    Possible verdicts for a submission.
    """

    PENDING = "PENDING"
    COMPILING = "COMPILING"
    RUNNING = "RUNNING"
    ACCEPTED = "ACCEPTED"
    WRONG_ANSWER = "WRONG_ANSWER"
    RUNTIME_ERROR = "RUNTIME_ERROR"
    TIME_LIMIT_EXCEEDED = "TIME_LIMIT_EXCEEDED"
    MEMORY_LIMIT_EXCEEDED = "MEMORY_LIMIT_EXCEEDED"
    COMPILATION_ERROR = "COMPILATION_ERROR"


class Submission(Base):
    """
    Represents a user's solution submission for a problem.
    """

    __tablename__ = "submissions"
    __table_args__ = (
        Index(
            "ix_submissions_user_id_created_at",
            "user_id",
            "created_at",
        ),
        Index(
            "ix_submissions_user_id_status",
            "user_id",
            "status",
        ),
        Index(
            "ix_submissions_user_problem_created_at",
            "user_id",
            "problem_id",
            "created_at",
        ),
        Index(
            "ix_submissions_user_status_created_at",
            "user_id",
            "status",
            "created_at",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    problem_id: Mapped[int] = mapped_column(
        ForeignKey("problems.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    language: Mapped[str] = mapped_column(
        nullable=False,
    )

    source_code: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    status: Mapped[SubmissionStatus] = mapped_column(
        SQLEnum(
            SubmissionStatus,
            name="submission_status",
        ),
        default=SubmissionStatus.PENDING,
        nullable=False,
    )

    execution_time_ms: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    memory_kb: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    user: Mapped[User] = relationship(
        "User",
        back_populates="submissions",
    )

    problem: Mapped[Problem] = relationship(
        "Problem",
        back_populates="submissions",
    )

    def __repr__(self) -> str:
        return (
            f"<Submission(id={self.id}, "
            f"user_id={self.user_id}, "
            f"problem_id={self.problem_id}, "
            f"status='{self.status.value}')>"
        )
