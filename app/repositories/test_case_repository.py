from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.test_case import TestCase


class TestCaseRepository:
    """
    Handles database operations for test cases.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        *,
        problem_id: int,
        input_data: str,
        expected_output: str,
        is_sample: bool,
    ) -> TestCase:
        """
        Create a new test case.
        """

        test_case = TestCase(
            problem_id=problem_id,
            input_data=input_data,
            expected_output=expected_output,
            is_sample=is_sample,
        )

        self.db.add(test_case)
        self.db.commit()
        self.db.refresh(test_case)

        return test_case

    def get_by_problem_id(
        self,
        problem_id: int,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[TestCase]:
        """
        Return all test cases for a problem.
        """

        stmt = (
            select(TestCase)
            .where(
                TestCase.problem_id == problem_id
            )
            .order_by(TestCase.id.asc())
        )

        if limit is not None:
            stmt = stmt.limit(limit)

        if offset is not None:
            stmt = stmt.offset(offset)

        return list(self.db.scalars(stmt).all())

    def count_by_problem_id(
        self,
        problem_id: int,
    ) -> int:
        """
        Return number of test cases for a problem.
        """

        stmt = (
            select(func.count())
            .select_from(TestCase)
            .where(
                TestCase.problem_id == problem_id
            )
        )

        return self.db.scalar(stmt) or 0