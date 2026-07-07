from sqlalchemy.orm import Session

from app.judge.docker_runner import DockerRunner
from app.models.submission import SubmissionStatus
from app.repositories.submission_repository import SubmissionRepository


class JudgeService:
    """
    Business logic for judging submissions.
    """

    def __init__(self, db: Session):
        self.repository = SubmissionRepository(db)
        self.runner = DockerRunner()

    def judge_submission(
        self,
        submission_id: int,
    ) -> None:
        """
        Judge a submission using Docker.
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

        if submission.language.lower() != "python":
            submission.status = SubmissionStatus.COMPILATION_ERROR
            self.repository.db.commit()

            print(
                f"[Judge] Unsupported language: {submission.language}"
            )
            return

        result = self.runner.run_python(
            submission.source_code
        )

        submission.execution_time_ms = (
            result.execution_time_ms
        )

        if result.exit_code == 0:
            submission.status = SubmissionStatus.ACCEPTED
        else:
            submission.status = SubmissionStatus.RUNTIME_ERROR

        self.repository.db.commit()

        print(
            f"[Judge] Finished submission {submission.id}"
        )

        print("STDOUT")
        print(result.stdout)

        print("STDERR")
        print(result.stderr)