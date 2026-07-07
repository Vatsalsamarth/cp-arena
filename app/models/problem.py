from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, Index, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Problem(Base):
    """
    Competitive programming problem.
    """

    __tablename__ = "problems"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        unique=True,
        nullable=False,
        index=True,
    )

    slug: Mapped[str] = mapped_column(
        String(200),
        unique=True,
        nullable=False,
        index=True,
    )

    statement: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    difficulty: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    submissions: Mapped[list["Submission"]] = relationship(
        "Submission",
        back_populates="problem",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    user_statuses: Mapped[list["UserProblemStatus"]] = relationship(
        "UserProblemStatus",
        back_populates="problem",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return f"<Problem(id={self.id}, title='{self.title}')>"
