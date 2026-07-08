from sqlalchemy.orm import Session

from app.core.exceptions import UserAlreadyExistsError
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
        if self.repository.get_by_username(user_create.username):
            raise UserAlreadyExistsError("Username already exists.")

        if self.repository.get_by_email(user_create.email):
            raise UserAlreadyExistsError("Email already exists.")

        hashed_password = hash_password(user_create.password)

        return self.repository.create(
            username=user_create.username,
            email=user_create.email,
            hashed_password=hashed_password,
        )
