from collections.abc import Generator

from sqlalchemy.orm import Session, sessionmaker

from app.db.database import engine

# Create a Session factory.
# Each request will receive a new Session instance.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a database session.

    A new session is created for every request.
    The session is automatically closed after the request completes.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
