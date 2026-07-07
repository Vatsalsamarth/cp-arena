from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TestCase(Base):
    """
    Test case belonging to a problem.
    """

    __tablename__ = "test_cases"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    problem_id: Mapped[int] = mapped_column(
        ForeignKey(
            "problems.id",
            ondelete="CASCADE",
        ),
        index=True,
        nullable=False,
    )

    input_data: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    expected_output: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    is_sample: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return (
            f"<TestCase(id={self.id}, "
            f"problem_id={self.problem_id})>"
        )