from sqlalchemy.orm import Session

from app.core.exceptions import ProblemNotFoundError
from app.models.test_case import TestCase
from app.repositories.problem_repository import ProblemRepository
from app.repositories.test_case_repository import (
    TestCaseRepository,
)
from app.schemas.test_case import TestCaseCreate


class TestCaseService:
    """
    Business logic for test cases.
    """

    def __init__(self, db: Session):
        self.problem_repository = ProblemRepository(db)
        self.test_case_repository = TestCaseRepository(db)

    def create_test_case(
        self,
        *,
        problem_id: int,
        test_case_create: TestCaseCreate,
    ) -> TestCase:
        """
        Create a test case for a problem.
        """

        problem = self.problem_repository.get_by_id(
            problem_id
        )

        if problem is None:
            raise ProblemNotFoundError(
                "Problem not found."
            )

        return self.test_case_repository.create(
            problem_id=problem.id,
            input_data=test_case_create.input_data,
            expected_output=test_case_create.expected_output,
            is_sample=test_case_create.is_sample,
        )

    def list_test_cases(
        self,
        *,
        problem_id: int,
    ) -> list[TestCase]:
        """
        Return all test cases for a problem.
        """

        problem = self.problem_repository.get_by_id(
            problem_id
        )

        if problem is None:
            raise ProblemNotFoundError(
                "Problem not found."
            )

        return self.test_case_repository.get_by_problem_id(
            problem_id
        )