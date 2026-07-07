from sqlalchemy.orm import Session

from app.models.submission import SubmissionStatus
from app.models.user import User
from app.repositories.submission_repository import (
    SubmissionRepository,
)
from app.schemas.user_stats import UserStatsResponse


class UserStatsService:
    """
    Business logic for user statistics.
    """

    def __init__(
        self,
        db: Session,
    ):
        self.repository = SubmissionRepository(db)

    def get_stats(
        self,
        *,
        current_user: User,
    ) -> UserStatsResponse:
        """
        Calculate statistics for a user.
        """

        total = self.repository.count_by_user(
            current_user.id
        )

        status_counts = self.repository.count_statuses_by_user(
            current_user.id
        )

        accepted = status_counts.get(
            SubmissionStatus.ACCEPTED,
            0,
        )
        wrong_answer = status_counts.get(
            SubmissionStatus.WRONG_ANSWER,
            0,
        )
        runtime_error = status_counts.get(
            SubmissionStatus.RUNTIME_ERROR,
            0,
        )
        compilation_error = status_counts.get(
            SubmissionStatus.COMPILATION_ERROR,
            0,
        )

        acceptance_rate = (
            (accepted / total) * 100
            if total > 0
            else 0.0
        )

        return UserStatsResponse(
            total_submissions=total,
            accepted=accepted,
            wrong_answer=wrong_answer,
            runtime_error=runtime_error,
            compilation_error=compilation_error,
            acceptance_rate=round(
                acceptance_rate,
                2,
            ),
        )