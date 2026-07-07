import time

from sqlalchemy.orm import Session

from app.models.submission import SubmissionStatus
from app.repositories.submission_repository import SubmissionRepository


class JudgeService:
    """
    Business logic for judging submissions.
    """

    def __init__(self, db: Session):
        self.repository = SubmissionRepository(db)

    def judge_submission(
        self,
        submission_id: int,
    ) -> None:
        """
        Judge a single submission.
        """

        submission = self.repository.get_by_id(
            submission_id
        )

        if submission is None:
            return

        submission.status = SubmissionStatus.RUNNING
        self.repository.db.commit()

        print(
            f"[Judge] Running submission {submission.id}"
        )

        #
        # Temporary simulation.
        # Will become Docker execution.
        #
        time.sleep(3)

        submission.status = SubmissionStatus.ACCEPTED

        self.repository.db.commit()

        print(
            f"[Judge] Accepted submission {submission.id}"
        )