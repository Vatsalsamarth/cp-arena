from logging.config import fileConfig

from sqlalchemy import create_engine, pool

import app.models.user_problem_status  # noqa: F401
from alembic import context
from app.core.config import settings
from app.db.base import Base

# Import all models so Alembic can discover them
from app.models.problem import Problem  # noqa: F401
from app.models.user import User  # noqa: F401

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Override the URL from alembic.ini using our application settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

print(f"[Alembic] Database URL: {settings.DATABASE_URL}")

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in offline mode."""

    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in online mode."""

    connectable = create_engine(
        settings.DATABASE_URL,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
