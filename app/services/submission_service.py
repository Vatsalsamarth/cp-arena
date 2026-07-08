import json

from sqlalchemy.orm import Session

from app.core.cache import invalidate_tracked, set_tracked
from app.core.exceptions import (
    ProblemNotFoundError,
    SubmissionNotFoundError,
)
from app.core.redis import redis_client
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

        problem = self.problem_repository.get_by_id(submission_create.problem_id)

        if problem is None:
            raise ProblemNotFoundError("Problem not found.")

        submission = self.submission_repository.create(
            user_id=current_user.id,
            problem_id=problem.id,
            language=submission_create.language,
            source_code=submission_create.source_code,
        )

        self.queue.enqueue_submission(submission.id)

        # Invalidate cached submission lists for users after creating a submission.
        try:
            invalidate_tracked(redis_client, "submissions:keys")
        except Exception:
            pass

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

        cache_key = ":".join(
            [
                "submissions",
                str(filters.user_id),
                str(getattr(filters, "language", None)),
                str(filters.status),
                str(filters.limit),
                str(filters.offset),
            ]
        )

        cached = redis_client.get(cache_key)

        if cached is not None:
            return json.loads(cached)

        items, total = self.submission_repository.list_all(filters)

        # Serialize submission fields for response and caching.
        items_payload = [
            {
                "id": s.id,
                "user_id": s.user_id,
                "problem_id": s.problem_id,
                "language": s.language,
                "source_code": s.source_code,
                "status": (
                    s.status.value if hasattr(s.status, "value") else str(s.status)
                ),
                "execution_time_ms": getattr(s, "execution_time_ms", None),
                "memory_kb": getattr(s, "memory_kb", None),
                "created_at": (
                    s.created_at.isoformat()
                    if getattr(s, "created_at", None) is not None
                    else None
                ),
            }
            for s in items
        ]

        limit = getattr(filters, "limit", 20)
        offset = getattr(filters, "offset", 0)

        payload = {
            "items": items_payload,
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_next": offset + limit < total,
        }

        set_tracked(
            redis_client=redis_client,
            tracking_set="submissions:keys",
            key=cache_key,
            value=json.dumps(payload),
            ex=15,
        )

        return payload

    def get_submission(
        self,
        *,
        submission_id: int,
        current_user: User,
    ) -> Submission:
        """
        Return a submission owned by the current user.
        """

        submission = self.submission_repository.get_by_id(submission_id)

        if submission is None:
            raise SubmissionNotFoundError("Submission not found.")

        if submission.user_id != current_user.id:
            raise SubmissionNotFoundError("Submission not found.")

        return submission
