from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.submission import Submission, SubmissionStatus
from app.schemas.submission import SubmissionFilters


class SubmissionRepository:
    """
    Handles all database operations for submissions.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        *,
        user_id: int,
        problem_id: int,
        language: str,
        source_code: str,
    ) -> Submission:
        """
        Create a new submission.
        """

        submission = Submission(
            user_id=user_id,
            problem_id=problem_id,
            language=language,
            source_code=source_code,
        )

        self.db.add(submission)
        self.db.commit()
        self.db.refresh(submission)

        return submission

    def get_by_id(
        self,
        submission_id: int,
    ) -> Submission | None:
        """
        Retrieve a submission by ID.
        """

        stmt = select(Submission).where(
            Submission.id == submission_id
        )

        return self.db.scalar(stmt)

    def list_all(
        self,
        filters: SubmissionFilters,
    ) -> tuple[list[Submission], int]:
        """
        Return filtered submissions together
        with the total number of matches.
        """

        stmt = select(Submission)

        count_stmt = (
            select(func.count())
            .select_from(Submission)
        )

        if filters.user_id is not None:
            condition = Submission.user_id == filters.user_id
            stmt = stmt.where(condition)
            count_stmt = count_stmt.where(condition)

        if filters.problem_id is not None:
            condition = Submission.problem_id == filters.problem_id
            stmt = stmt.where(condition)
            count_stmt = count_stmt.where(condition)

        if filters.status is not None:
            condition = Submission.status == filters.status
            stmt = stmt.where(condition)
            count_stmt = count_stmt.where(condition)

        stmt = (
            stmt.order_by(Submission.created_at.desc())
            .limit(filters.limit)
            .offset(filters.offset)
        )

        items = list(self.db.scalars(stmt).all())

        total = self.db.scalar(count_stmt) or 0

        return items, total

    def count_by_user(
        self,
        user_id: int,
    ) -> int:
        """
        Count total submissions by a user.
        """

        stmt = (
            select(func.count())
            .select_from(Submission)
            .where(
                Submission.user_id == user_id
            )
        )

        return self.db.scalar(stmt) or 0

    def count_by_user_and_status(
        self,
        *,
        user_id: int,
        status: SubmissionStatus,
    ) -> int:
        """
        Count submissions by user and status.
        """

        stmt = (
            select(func.count())
            .select_from(Submission)
            .where(
                Submission.user_id == user_id,
                Submission.status == status,
            )
        )

        return self.db.scalar(stmt) or 0