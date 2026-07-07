from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class UserService:
    """
    Contains business logic related to users.
    """

    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def create_user(self, user_create: UserCreate) -> User:
        """
        Create a new user after validating business rules.
        """

        existing_username = self.repository.get_by_username(
            user_create.username
        )
        if existing_username is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already exists.",
            )

        existing_email = self.repository.get_by_email(
            user_create.email
        )
        if existing_email is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists.",
            )

        hashed_password = hash_password(user_create.password)

        return self.repository.create(
            username=user_create.username,
            email=user_create.email,
            hashed_password=hashed_password,
        )