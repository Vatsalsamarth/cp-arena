from datetime import datetime

from sqlalchemy.orm import Session

from app.models.problem import Problem
from app.models.test_case import TestCase as TestCaseModel
from app.models.user import User
from app.models.user_problem_status import UserProblemStatus
from app.repositories.problem_repository import ProblemRepository
from app.schemas.test_case import TestCaseCreate as TestCaseCreateSchema
from app.services.test_case_service import TestCaseService as TestCaseServiceClass
from app.services.user_problem_status_service import UserProblemStatusService

TestCaseModel.__test__ = False
TestCaseCreateSchema.__test__ = False  # type: ignore[attr-defined]
TestCaseServiceClass.__test__ = False  # type: ignore[attr-defined]


def create_user(db: Session, username: str, email: str) -> User:
    user = User(username=username, email=email, hashed_password="hashed")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_problem(db: Session, title: str, slug: str, difficulty: int) -> Problem:
    problem = Problem(
        title=title, slug=slug, statement="statement", difficulty=difficulty
    )
    db.add(problem)
    db.commit()
    db.refresh(problem)
    return problem


def create_user_problem_status(
    db: Session, user_id: int, problem_id: int, solved_at: datetime | None = None
) -> UserProblemStatus:
    status = UserProblemStatus(user_id=user_id, problem_id=problem_id)
    if solved_at is not None:
        status.first_solved_at = solved_at  # type: ignore[assignment]
    db.add(status)
    db.commit()
    db.refresh(status)
    return status


def create_test_case_record(db: Session, problem_id: int, index: int) -> TestCaseModel:
    test_case = TestCaseModel(
        problem_id=problem_id,
        input_data=f"input-{index}",
        expected_output=f"output-{index}",
        is_sample=False,
    )
    db.add(test_case)
    db.commit()
    db.refresh(test_case)
    return test_case


def test_get_solved_problems_pagination(db: Session):
    user = create_user(db, "alice", "alice@example.com")
    problems = [
        create_problem(db, "Alpha", "alpha", 1000),
        create_problem(db, "Bravo", "bravo", 1200),
        create_problem(db, "Charlie", "charlie", 1400),
        create_problem(db, "Delta", "delta", 1600),
    ]

    for problem in problems:
        create_user_problem_status(db, user.id, problem.id)

    service = UserProblemStatusService(db)
    response = service.get_solved_problems(
        current_user=user,
        limit=2,
        offset=1,
        sort_by="problem_title",
        order="asc",
    )

    assert response.total == 4
    assert response.limit == 2
    assert response.offset == 1
    assert response.has_next is True
    assert len(response.items) == 2
    assert response.items[0].title == "Bravo"
    assert response.items[1].title == "Charlie"


def test_get_leaderboard_pagination(db: Session):
    users = [
        create_user(db, "user1", "user1@example.com"),
        create_user(db, "user2", "user2@example.com"),
        create_user(db, "user3", "user3@example.com"),
    ]
    problems = [
        create_problem(db, "P1", "p1", 1000),
        create_problem(db, "P2", "p2", 1200),
        create_problem(db, "P3", "p3", 1400),
    ]

    create_user_problem_status(db, users[0].id, problems[0].id)
    create_user_problem_status(db, users[0].id, problems[1].id)
    create_user_problem_status(db, users[1].id, problems[0].id)
    create_user_problem_status(db, users[2].id, problems[0].id)
    create_user_problem_status(db, users[2].id, problems[1].id)
    create_user_problem_status(db, users[2].id, problems[2].id)

    service = UserProblemStatusService(db)
    response = service.get_leaderboard(
        limit=2,
        offset=0,
        sort_by="solved_count",
        order="desc",
    )

    assert response.total == 3
    assert response.limit == 2
    assert response.offset == 0
    assert response.has_next is True
    assert len(response.items) == 2
    assert response.items[0].score == 3
    assert response.items[1].score == 2
    assert response.items[0].rank == 1
    assert response.items[1].rank == 2

    page_two = service.get_leaderboard(
        limit=2,
        offset=2,
        sort_by="solved_count",
        order="desc",
    )

    assert page_two.total == 3
    assert page_two.limit == 2
    assert page_two.offset == 2
    assert page_two.has_next is False
    assert len(page_two.items) == 1
    assert page_two.items[0].rank == 3
    assert page_two.items[0].score == 1


def test_list_test_cases_pagination(db: Session):
    problem = create_problem(db, "Problem X", "problem-x", 1500)
    repository = ProblemRepository(db)
    assert repository.get_by_id(problem.id) is not None

    service = TestCaseServiceClass(db)
    for index in range(5):
        service.create_test_case(
            problem_id=problem.id,
            test_case_create=TestCaseCreateSchema(
                input_data=f"input-{index}",
                expected_output=f"output-{index}",
                is_sample=False,
            ),
        )

    response = service.list_test_cases(
        problem_id=problem.id,
        limit=2,
        offset=2,
    )

    assert response.total == 5
    assert response.limit == 2
    assert response.offset == 2
    assert response.has_next is True
    assert len(response.items) == 2
    assert response.items[0].input_data == "input-2"
    assert response.items[1].input_data == "input-3"
