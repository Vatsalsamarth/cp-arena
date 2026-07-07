from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.test_case import TestCase
from app.schemas.test_case import (
    TestCaseCreate,
    TestCaseListResponse,
    TestCaseResponse,
)
from app.services.test_case_service import TestCaseService


router = APIRouter(
    prefix="/problems",
    tags=["Test Cases"],
)


@router.post(
    "/{problem_id}/testcases",
    response_model=TestCaseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_test_case(
    problem_id: int,
    test_case_create: TestCaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
 ) -> TestCase:
    """
    Create a test case for a problem.
    """

    service = TestCaseService(db)

    return service.create_test_case(
        problem_id=problem_id,
        test_case_create=test_case_create,
    )


@router.get(
    "/{problem_id}/testcases",
    response_model=TestCaseListResponse,
)
def list_test_cases(
    problem_id: int,
    db: Session = Depends(get_db),
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
) -> TestCaseListResponse:
    """
    List all test cases for a problem.
    """

    service = TestCaseService(db)

    return service.list_test_cases(
        problem_id=problem_id,
        limit=limit,
        offset=offset,
    )