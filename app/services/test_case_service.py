from sqlalchemy.orm import Session

from app.repositories.test_case_repository import (
    TestCaseRepository,
)


class TestCaseService:
    """
    Business logic for test cases.
    """

    def __init__(self, db: Session):
        self.repository = TestCaseRepository(db)

    def get_problem_test_cases(
        self,
        problem_id: int,
    ):
        return self.repository.get_by_problem_id(
            problem_id
        )