from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.

    Every database model in the application should inherit from this class.
    Example:

        class User(Base):
            ...

    SQLAlchemy uses this base class to keep track of all mapped tables.
    """

    pass
