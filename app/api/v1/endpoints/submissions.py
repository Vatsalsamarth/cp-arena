from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.db.session import get_db
from app.models.submission import SubmissionStatus
from app.models.user import User
from app.schemas.submission import (
    SubmissionCreate,
    SubmissionFilters,
    SubmissionListResponse,
    SubmissionResponse,
)
from app.services.submission_service import SubmissionService

router = APIRouter(
    prefix="/submissions",
    tags=["Submissions"],
)


@router.post(
    "",
    response_model=SubmissionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_submission(
    submission: SubmissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> SubmissionResponse:
    service = SubmissionService(db)

    return service.create_submission(
        current_user=current_user,
        submission_create=submission,
    )


@router.get(
    "",
    response_model=SubmissionListResponse,
)
def list_submissions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    status_filter: SubmissionStatus | None = Query(
        default=None,
        alias="status",
    ),
    problem_id: int | None = Query(
        default=None,
        gt=0,
    ),
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
) -> SubmissionListResponse:
    service = SubmissionService(db)

    filters = SubmissionFilters(
        status=status_filter,
        problem_id=problem_id,
        limit=limit,
        offset=offset,
    )

    return service.list_submissions(
        current_user=current_user,
        filters=filters,
    )


@router.get(
    "/{submission_id}",
    response_model=SubmissionResponse,
)
def get_submission(
    submission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> SubmissionResponse:
    service = SubmissionService(db)

    return service.get_submission(
        submission_id=submission_id,
        current_user=current_user,
    )
