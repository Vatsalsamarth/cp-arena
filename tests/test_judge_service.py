from sqlalchemy import select
from sqlalchemy.orm import Session

from app.judge.execution_result import ExecutionResult
from app.models.problem import Problem
from app.models.submission import Submission, SubmissionStatus
from app.models.test_case import TestCase as TestCaseModel
from app.models.user import User
from app.models.user_problem_status import UserProblemStatus
from app.services.judge_service import JudgeService


class FakeRunner:
    def __init__(
        self,
        stdout: str,
        stderr: str = "",
        exit_code: int = 0,
        execution_time_ms: int = 5,
    ):
        self._result = ExecutionResult(
            stdout=stdout,
            stderr=stderr,
            exit_code=exit_code,
            execution_time_ms=execution_time_ms,
        )

    def run_python(self, source_code: str, stdin: str = "") -> ExecutionResult:
        return self._result


def create_submission_with_test_case(db: Session, stdout: str, exit_code: int = 0) -> tuple[Submission, User, Problem]:
    user = User(
        username="judgeuser",
        email="judgeuser@example.com",
        hashed_password="hashed",
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    problem = Problem(
        title="Judge Problem",
        slug="judge-problem",
        statement="Judge this code.",
        difficulty=1200,
    )
    db.add(problem)
    db.commit()
    db.refresh(problem)

    test_case = TestCaseModel(
        problem_id=problem.id,
        input_data="1 2",
        expected_output="3",
        is_sample=False,
    )
    db.add(test_case)
    db.commit()
    db.refresh(test_case)

    submission = Submission(
        user_id=user.id,
        problem_id=problem.id,
        language="python",
        source_code="print(sum(map(int, input().split())))",
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)

    return submission, user, problem


def test_judge_service_accepts_correct_output(db: Session):
    submission, user, problem = create_submission_with_test_case(
        db,
        stdout="3\n",
        exit_code=0,
    )

    fake_runner = FakeRunner(stdout="3\n", exit_code=0)
    service = JudgeService(db, runner=fake_runner)
    service.judge_submission(submission.id)

    db.refresh(submission)
    assert submission.status == SubmissionStatus.ACCEPTED
    assert submission.execution_time_ms == 5

    solved_status = db.scalar(
        select(UserProblemStatus.id).where(
            UserProblemStatus.user_id == user.id,
            UserProblemStatus.problem_id == problem.id,
        )
    )
    assert solved_status is not None


def test_judge_service_marks_wrong_answer(db: Session):
    submission, user, problem = create_submission_with_test_case(
        db,
        stdout="4\n",
        exit_code=0,
    )

    fake_runner = FakeRunner(stdout="4\n", exit_code=0)
    service = JudgeService(db, runner=fake_runner)
    service.judge_submission(submission.id)

    db.refresh(submission)
    assert submission.status == SubmissionStatus.WRONG_ANSWER

    solved_status = db.scalar(
        select(UserProblemStatus.id).where(
            UserProblemStatus.user_id == user.id,
            UserProblemStatus.problem_id == problem.id,
        )
    )
    assert solved_status is None
