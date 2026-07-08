from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.test_case import ProblemTestCase


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
    ) -> ProblemTestCase:
        """
        Create a new test case.
        """

        test_case = ProblemTestCase(
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
    ) -> list[ProblemTestCase]:
        """
        Return all test cases for a problem.
        """

        stmt = (
            select(ProblemTestCase)
            .where(ProblemTestCase.problem_id == problem_id)
            .order_by(ProblemTestCase.id.asc())
        )

        if limit is not None:
            stmt = stmt.limit(limit)

        if offset is not None:
            stmt = stmt.offset(offset)

        return list(self.db.scalars(stmt).all())

    def list_by_problem_id_paginated(
        self,
        *,
        problem_id: int,
        limit: int,
        offset: int,
    ) -> tuple[list[ProblemTestCase], int]:
        """
        Return paginated test cases and exact total for a problem.

        Uses a limit+1 probe to avoid COUNT on terminal pages.
        """

        stmt = (
            select(ProblemTestCase)
            .where(ProblemTestCase.problem_id == problem_id)
            .order_by(ProblemTestCase.id.asc())
            .limit(limit + 1)
            .offset(offset)
        )

        rows = list(self.db.scalars(stmt).all())
        has_next = len(rows) > limit
        items = rows[:limit]

        if has_next:
            total = self.count_by_problem_id(problem_id)
        elif items:
            total = offset + len(items)
        elif offset == 0:
            total = 0
        else:
            total = self.count_by_problem_id(problem_id)

        return items, total

    def count_by_problem_id(
        self,
        problem_id: int,
    ) -> int:
        """
        Return number of test cases for a problem.
        """

        stmt = (
            select(func.count())
            .select_from(ProblemTestCase)
            .where(ProblemTestCase.problem_id == problem_id)
        )

        return self.db.scalar(stmt) or 0
