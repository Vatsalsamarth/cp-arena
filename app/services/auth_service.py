from sqlalchemy.orm import Session

from app.core.exceptions import InvalidCredentialsError
from app.core.jwt import create_access_token
from app.core.security import verify_password
from app.repositories.user_repository import UserRepository


class AuthService:
    """
    Contains business logic related to authentication.
    """

    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def authenticate_user(
        self,
        username: str,
        password: str,
    ) -> dict[str, str]:
        """
        Authenticate a user and generate an access token.
        """

        user = self.repository.get_by_username(username)

        if user is None:
            raise InvalidCredentialsError("Invalid username or password.")

        if not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError("Invalid username or password.")

        access_token = create_access_token(
            subject=user.username,
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }