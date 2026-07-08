"""add performance indexes

Revision ID: 72a1b3f4d9e1
Revises: d3324480aed7
Create Date: 2026-07-08 13:00:00.000000

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "72a1b3f4d9e1"
down_revision: str | Sequence[str] | None = "d3324480aed7"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_index(
        op.f("ix_problems_difficulty"),
        "problems",
        ["difficulty"],
        unique=False,
    )
    op.create_index(
        op.f("ix_submissions_user_id_created_at"),
        "submissions",
        ["user_id", "created_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_submissions_user_id_status"),
        "submissions",
        ["user_id", "status"],
        unique=False,
    )
    op.create_index(
        op.f("ix_user_problem_status_user_id_first_solved_at"),
        "user_problem_status",
        ["user_id", "first_solved_at"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        op.f("ix_user_problem_status_user_id_first_solved_at"),
        table_name="user_problem_status",
    )
    op.drop_index(
        op.f("ix_submissions_user_id_status"),
        table_name="submissions",
    )
    op.drop_index(
        op.f("ix_submissions_user_id_created_at"),
        table_name="submissions",
    )
    op.drop_index(
        op.f("ix_problems_difficulty"),
        table_name="problems",
    )
