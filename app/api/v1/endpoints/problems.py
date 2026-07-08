from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.problem import (
    ProblemCreate,
    ProblemListResponse,
    ProblemResponse,
    ProblemUpdate,
)
from app.services.problem_service import ProblemService

router = APIRouter(
    prefix="/problems",
    tags=["Problems"],
)


@router.post(
    "",
    response_model=ProblemResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_problem(
    problem: ProblemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ProblemResponse:
    service = ProblemService(db)
    return service.create_problem(problem)


@router.get(
    "",
    response_model=ProblemListResponse,
)
def list_problems(
    db: Session = Depends(get_db),
    title: str | None = Query(
        default=None,
        description="Search by title.",
    ),
    slug: str | None = Query(
        default=None,
        description="Search by slug.",
    ),
    min_difficulty: int | None = Query(
        default=None,
        ge=800,
        le=3500,
    ),
    max_difficulty: int | None = Query(
        default=None,
        ge=800,
        le=3500,
    ),
    sort_by: Literal[
        "id",
        "difficulty",
        "title",
    ] = Query(default="id"),
    order: Literal[
        "asc",
        "desc",
    ] = Query(default="asc"),
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
) -> ProblemListResponse:
    """
    Return filtered, sorted and paginated problems.
    """

    service = ProblemService(db)

    return service.list_problems(
        title=title,
        slug=slug,
        min_difficulty=min_difficulty,
        max_difficulty=max_difficulty,
        sort_by=sort_by,
        order=order,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/{slug}",
    response_model=ProblemResponse,
)
def get_problem(
    slug: str,
    db: Session = Depends(get_db),
) -> ProblemResponse:
    service = ProblemService(db)
    return service.get_problem_or_raise(slug)


@router.put(
    "/{slug}",
    response_model=ProblemResponse,
)
def update_problem(
    slug: str,
    problem: ProblemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ProblemResponse:
    service = ProblemService(db)

    return service.update_problem(
        slug=slug,
        problem_update=problem,
    )


@router.delete(
    "/{slug}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_problem(
    slug: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Response:
    service = ProblemService(db)
    service.delete_problem(slug)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
