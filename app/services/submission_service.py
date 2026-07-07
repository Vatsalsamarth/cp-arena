from sqlalchemy.orm import Session

from app.core.exceptions import (
    ProblemNotFoundError,
    SubmissionNotFoundError,
)
from app.models.submission import Submission
from app.models.user import User
from app.queue.redis_queue import RedisQueue
from app.repositories.problem_repository import ProblemRepository
from app.repositories.submission_repository import SubmissionRepository
from app.schemas.submission import (
    SubmissionCreate,
    SubmissionFilters,
)


class SubmissionService:
    """
    Contains business logic for submissions.
    """

    def __init__(self, db: Session):
        self.problem_repository = ProblemRepository(db)
        self.submission_repository = SubmissionRepository(db)
        self.queue = RedisQueue()

    def create_submission(
        self,
        *,
        current_user: User,
        submission_create: SubmissionCreate,
    ) -> Submission:
        """
        Create a new submission and enqueue it for judging.
        """

        problem = self.problem_repository.get_by_id(
            submission_create.problem_id
        )

        if problem is None:
            raise ProblemNotFoundError(
                "Problem not found."
            )

        submission = self.submission_repository.create(
            user_id=current_user.id,
            problem_id=problem.id,
            language=submission_create.language,
            source_code=submission_create.source_code,
        )

        self.queue.enqueue_submission(
            submission.id
        )

        return submission

    def list_submissions(
        self,
        *,
        current_user: User,
        filters: SubmissionFilters,
    ) -> dict:
        """
        Return the authenticated user's submissions.
        """

        filters.user_id = current_user.id

        items, total = self.submission_repository.list_all(
            filters
        )

        return {
            "items": items,
            "total": total,
            "limit": filters.limit,
            "offset": filters.offset,
            "has_next": (
                filters.offset + filters.limit < total
            ),
        }

    def get_submission(
        self,
        *,
        submission_id: int,
        current_user: User,
    ) -> Submission:
        """
        Return a submission owned by the current user.
        """

        submission = self.submission_repository.get_by_id(
            submission_id
        )

        if submission is None:
            raise SubmissionNotFoundError(
                "Submission not found."
            )

        if submission.user_id != current_user.id:
            raise SubmissionNotFoundError(
                "Submission not found."
            )

        return submission