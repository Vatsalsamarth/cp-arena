from sqlalchemy import create_engine

from app.core.config import settings

# Create a single SQLAlchemy Engine for the entire application.
# The Engine manages the database connection pool.
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
)
