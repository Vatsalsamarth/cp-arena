from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.schemas.user_stats import UserStatsResponse
from app.services.user_service import UserService
from app.services.user_stats_service import UserStatsService


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
) -> UserResponse:
    """
    Create a new user.
    """

    service = UserService(db)

    created_user = service.create_user(
        user
    )

    return created_user


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """
    Return the currently authenticated user's profile.
    """

    return current_user


@router.get(
    "/me/stats",
    response_model=UserStatsResponse,
)
def get_my_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserStatsResponse:
    """
    Return submission statistics for the current user.
    """

    service = UserStatsService(db)

    return service.get_stats(
        current_user=current_user,
    )