from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.test_case import TestCase


class TestCaseRepository:
    """
    Handles database operations for test cases.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_by_problem_id(
        self,
        problem_id: int,
    ) -> list[TestCase]:
        """
        Return every test case belonging to a problem.
        """

        stmt = (
            select(TestCase)
            .where(TestCase.problem_id == problem_id)
            .order_by(TestCase.id.asc())
        )

        return list(self.db.scalars(stmt).all())