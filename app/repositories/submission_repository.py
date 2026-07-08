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

        stmt = select(Submission).where(Submission.id == submission_id)

        return self.db.scalar(stmt)

    def list_all(
        self,
        filters: SubmissionFilters,
    ) -> tuple[list[Submission], int]:
        """
        Return filtered submissions together
        with the total number of matches.
        """

        conditions = []

        if filters.user_id is not None:
            conditions.append(Submission.user_id == filters.user_id)

        if filters.problem_id is not None:
            conditions.append(Submission.problem_id == filters.problem_id)

        if filters.status is not None:
            conditions.append(Submission.status == filters.status)

        stmt = select(Submission)
        count_stmt = select(func.count()).select_from(Submission)

        for condition in conditions:
            stmt = stmt.where(condition)
            count_stmt = count_stmt.where(condition)

        paginated_stmt = (
            stmt.order_by(
                Submission.created_at.desc(),
                Submission.id.desc(),
            )
            .limit(filters.limit + 1)
            .offset(filters.offset)
        )

        rows = list(self.db.scalars(paginated_stmt).all())
        has_next = len(rows) > filters.limit
        items = rows[: filters.limit]

        if has_next:
            total = self.db.scalar(count_stmt) or 0
        elif items:
            total = filters.offset + len(items)
        elif filters.offset == 0:
            total = 0
        else:
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
            .where(Submission.user_id == user_id)
        )

        return self.db.scalar(stmt) or 0

    def count_statuses_by_user(
        self,
        user_id: int,
    ) -> dict[SubmissionStatus, int]:
        """
        Count submissions grouped by status for a user.
        """

        stmt = (
            select(
                Submission.status,
                func.count().label("status_count"),
            )
            .where(Submission.user_id == user_id)
            .group_by(Submission.status)
        )

        rows = self.db.execute(stmt).all()

        return {row.status: int(row.status_count) for row in rows}

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
