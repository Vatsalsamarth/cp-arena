from typing import Any

from sqlalchemy.orm import Session

from app.judge.docker_runner import DockerRunner
from app.judge.output_checker import OutputChecker
from app.models.submission import SubmissionStatus
from app.repositories.submission_repository import SubmissionRepository
from app.repositories.test_case_repository import TestCaseRepository
from app.repositories.user_problem_status_repository import UserProblemStatusRepository


class JudgeService:
    """
    Business logic for judging submissions.
    """

    def __init__(
        self,
        db: Session,
        runner: Any | None = None,
        output_checker: Any | None = None,
    ):
        self.submission_repository = SubmissionRepository(db)
        self.test_case_repository = TestCaseRepository(db)
        self.user_problem_status_repository = UserProblemStatusRepository(db)

        self.runner = runner or DockerRunner()
        self.output_checker = output_checker or OutputChecker()

    def judge_submission(
        self,
        submission_id: int,
    ) -> None:
        """
        Judge a submission against all test cases.
        """

        submission = self.submission_repository.get_by_id(submission_id)

        if submission is None:
            return

        submission.status = SubmissionStatus.RUNNING
        self.submission_repository.db.commit()

        print(f"[Judge] Running submission {submission.id}")

        if submission.language.lower() != "python":
            submission.status = SubmissionStatus.COMPILATION_ERROR

            self.submission_repository.db.commit()

            print(f"[Judge] Unsupported language: {submission.language}")

            return

        test_cases = self.test_case_repository.get_by_problem_id(submission.problem_id)

        if not test_cases:
            submission.status = SubmissionStatus.WRONG_ANSWER

            self.submission_repository.db.commit()

            print("[Judge] No test cases found.")

            return

        for test_case in test_cases:
            result = self.runner.run_python(
                source_code=submission.source_code,
                stdin=test_case.input_data,
            )

            submission.execution_time_ms = result.execution_time_ms

            if result.exit_code != 0:
                submission.status = SubmissionStatus.RUNTIME_ERROR

                self.submission_repository.db.commit()

                print(f"[Judge] Runtime error on test case {test_case.id}")

                return

            passed = self.output_checker.compare(
                actual=result.stdout,
                expected=test_case.expected_output,
            )

            if not passed:
                submission.status = SubmissionStatus.WRONG_ANSWER

                self.submission_repository.db.commit()

                print(f"[Judge] Wrong answer on test case {test_case.id}")

                return

        submission.status = SubmissionStatus.ACCEPTED

        self.submission_repository.db.commit()
        self.user_problem_status_repository.create_if_missing(
            user_id=submission.user_id,
            problem_id=submission.problem_id,
        )

        print(f"[Judge] Accepted submission {submission.id}")
