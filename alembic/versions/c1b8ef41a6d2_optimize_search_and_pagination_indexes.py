"""optimize search and pagination indexes

Revision ID: c1b8ef41a6d2
Revises: 72a1b3f4d9e1, 7b39c92c606a
Create Date: 2026-07-08 15:05:00.000000

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c1b8ef41a6d2"
down_revision: str | Sequence[str] | None = (
    "72a1b3f4d9e1",
    "7b39c92c606a",
)
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_index(
        op.f("ix_problems_difficulty_id"),
        "problems",
        ["difficulty", "id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_submissions_user_problem_created_at"),
        "submissions",
        ["user_id", "problem_id", "created_at"],
        unique=False,
    )

    op.create_index(
        op.f("ix_submissions_user_status_created_at"),
        "submissions",
        ["user_id", "status", "created_at"],
        unique=False,
    )

    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
        op.execute(
            """
            CREATE INDEX IF NOT EXISTS ix_problems_title_trgm
            ON problems USING gin (lower(title) gin_trgm_ops)
            """
        )
        op.execute(
            """
            CREATE INDEX IF NOT EXISTS ix_problems_slug_trgm
            ON problems USING gin (lower(slug) gin_trgm_ops)
            """
        )


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        op.execute("DROP INDEX IF EXISTS ix_problems_slug_trgm")
        op.execute("DROP INDEX IF EXISTS ix_problems_title_trgm")

    op.drop_index(
        op.f("ix_submissions_user_status_created_at"),
        table_name="submissions",
    )

    op.drop_index(
        op.f("ix_submissions_user_problem_created_at"),
        table_name="submissions",
    )

    op.drop_index(
        op.f("ix_problems_difficulty_id"),
        table_name="problems",
    )
