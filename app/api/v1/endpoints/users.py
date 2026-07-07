from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.schemas.user_problem_status import (
    LeaderboardListResponse,
    SolvedProblemListResponse,
)
from app.schemas.user_stats import UserStatsResponse
from app.services.user_problem_status_service import UserProblemStatusService
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
) -> User:
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
) -> User:
    """
    Return the currently authenticated user's profile.
    """

    return current_user


@router.get(
    "/me/solved",
    response_model=SolvedProblemListResponse,
)
def get_my_solved_problems(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    sort_by: Literal[
        "first_solved_at",
        "problem_title",
    ] = Query(default="first_solved_at"),
    order: Literal[
        "asc",
        "desc",
    ] = Query(default="desc"),
    limit: Annotated[
        int,
        Query(
            ge=1,
            le=100,
        ),
    ] = 20,
    offset: Annotated[
        int,
        Query(
            ge=0,
        ),
    ] = 0,
) -> SolvedProblemListResponse:
    """
    Return the list of problems the current user has solved.
    """

    service = UserProblemStatusService(db)

    return service.get_solved_problems(
        current_user=current_user,
        limit=limit,
        offset=offset,
        sort_by=sort_by,
        order=order,
    )


@router.get(
    "/leaderboard",
    response_model=LeaderboardListResponse,
)
def get_leaderboard(
    db: Session = Depends(get_db),
    sort_by: Literal[
        "solved_count",
        "username",
    ] = Query(default="solved_count"),
    order: Literal[
        "asc",
        "desc",
    ] = Query(default="desc"),
    limit: Annotated[
        int,
        Query(
            ge=1,
            le=100,
        ),
    ] = 20,
    offset: Annotated[
        int,
        Query(
            ge=0,
        ),
    ] = 0,
) -> LeaderboardListResponse:
    """
    Return the current user leaderboard.
    """

    service = UserProblemStatusService(db)

    return service.get_leaderboard(
        limit=limit,
        offset=offset,
        sort_by=sort_by,
        order=order,
    )


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