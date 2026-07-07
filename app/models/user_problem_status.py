from __future__ import annotations

from sqlalchemy import DateTime, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base


class UserProblemStatus(Base):
    __tablename__ = "user_problem_status"
    __table_args__ = (
        UniqueConstraint("user_id", "problem_id", name="uq_user_problem_status_user_problem"),
        Index(
            "ix_user_problem_status_user_id_first_solved_at",
            "user_id",
            "first_solved_at",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

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

    first_solved_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    user = relationship("User", back_populates="solved_problems")
    problem = relationship("Problem", back_populates="user_statuses")
