from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.problem import Problem
from app.models.user import User
from app.models.user_problem_status import UserProblemStatus


def create_user_and_login(client: TestClient, username: str, email: str, password: str) -> str:
    create_resp = client.post(
        "/api/users",
        json={
            "username": username,
            "email": email,
            "password": password,
        },
    )
    assert create_resp.status_code == 201

    login_resp = client.post(
        "/api/auth/login",
        json={
            "username": username,
            "password": password,
        },
    )
    assert login_resp.status_code == 200
    return login_resp.json()["access_token"]


def test_users_solved_and_leaderboard_endpoints(client: TestClient, db: Session):
    token = create_user_and_login(
        client,
        username="apiuser",
        email="apiuser@example.com",
        password="strongpass",
    )
    auth_headers = {"Authorization": f"Bearer {token}"}

    problem1 = Problem(title="APITest1", slug="apitest1", statement="stmt", difficulty=1000)
    problem2 = Problem(title="APITest2", slug="apitest2", statement="stmt", difficulty=1200)
    db.add_all([problem1, problem2])
    db.commit()
    db.refresh(problem1)
    db.refresh(problem2)

    user_id = db.scalar(
        select(User.id).where(User.username == "apiuser")
    )
    assert user_id is not None
    db.add_all([
        UserProblemStatus(user_id=user_id, problem_id=problem1.id),
        UserProblemStatus(user_id=user_id, problem_id=problem2.id),
    ])
    db.commit()

    solved_resp = client.get(
        "/api/users/me/solved",
        headers=auth_headers,
        params={"limit": 1, "offset": 0, "sort_by": "problem_title", "order": "asc"},
    )
    assert solved_resp.status_code == 200
    solved_data = solved_resp.json()
    assert solved_data["total"] == 2
    assert solved_data["limit"] == 1
    assert solved_data["offset"] == 0
    assert solved_data["has_next"] is True
    assert solved_data["items"][0]["slug"] == "apitest1"

    leaderboard_resp = client.get(
        "/api/users/leaderboard",
        headers=auth_headers,
        params={"limit": 5, "offset": 0, "sort_by": "solved_count", "order": "desc"},
    )
    assert leaderboard_resp.status_code == 200
    leaderboard_data = leaderboard_resp.json()
    assert leaderboard_data["total"] == 1
    assert leaderboard_data["items"][0]["score"] == 2


def test_problem_crud_endpoints(client: TestClient):
    token = create_user_and_login(
        client,
        username="problemuser",
        email="problemuser@example.com",
        password="strongpass",
    )
    headers = {"Authorization": f"Bearer {token}"}

    create_resp = client.post(
        "/api/problems",
        json={
            "title": "CRUD Problem",
            "slug": "crud-problem",
            "statement": "Example statement.",
            "difficulty": 1500,
        },
        headers=headers,
    )
    assert create_resp.status_code == 201
    problem = create_resp.json()
    assert problem["title"] == "CRUD Problem"
    assert problem["slug"] == "crud-problem"

    get_resp = client.get(f"/api/problems/{problem['slug']}")
    assert get_resp.status_code == 200
    get_data = get_resp.json()
    assert get_data["id"] == problem["id"]

    list_resp = client.get(
        "/api/problems",
        params={"title": "CRUD"},
    )
    assert list_resp.status_code == 200
    assert any(item["slug"] == "crud-problem" for item in list_resp.json()["items"])

    update_resp = client.put(
        f"/api/problems/{problem['slug']}",
        json={
            "title": "CRUD Problem Updated",
            "slug": "crud-problem-updated",
            "statement": "Updated statement that passes validation.",
            "difficulty": 1600,
        },
        headers=headers,
    )
    assert update_resp.status_code == 200
    updated = update_resp.json()
    assert updated["slug"] == "crud-problem-updated"
    assert updated["difficulty"] == 1600

    delete_resp = client.delete(
        f"/api/problems/{updated['slug']}",
        headers=headers,
    )
    assert delete_resp.status_code == 204

    get_deleted_resp = client.get(f"/api/problems/{updated['slug']}")
    assert get_deleted_resp.status_code == 404


def test_test_case_and_submission_endpoints(client: TestClient, db: Session):
    token = create_user_and_login(
        client,
        username="submituser",
        email="submituser@example.com",
        password="strongpass",
    )
    headers = {"Authorization": f"Bearer {token}"}

    problem_resp = client.post(
        "/api/problems",
        json={
            "title": "Submit Problem",
            "slug": "submit-problem",
            "statement": "Solve this problem with code.",
            "difficulty": 1200,
        },
        headers=headers,
    )
    assert problem_resp.status_code == 201
    problem_id = problem_resp.json()["id"]

    testcase_resp = client.post(
        f"/api/problems/{problem_id}/testcases",
        json={
            "input_data": "1 2",
            "expected_output": "3",
            "is_sample": False,
        },
        headers=headers,
    )
    assert testcase_resp.status_code == 201
    testcase_data = testcase_resp.json()
    assert testcase_data["problem_id"] == problem_id

    list_tc_resp = client.get(
        f"/api/problems/{problem_id}/testcases",
        params={"limit": 1, "offset": 0},
    )
    assert list_tc_resp.status_code == 200
    tc_data = list_tc_resp.json()
    assert tc_data["total"] == 1
    assert tc_data["limit"] == 1
    assert tc_data["offset"] == 0
    assert tc_data["has_next"] is False
    assert tc_data["items"][0]["input_data"] == "1 2"

    submission_resp = client.post(
        "/api/submissions",
        json={
            "problem_id": problem_id,
            "language": "python",
            "source_code": "print(sum(map(int, input().split())))",
        },
        headers=headers,
    )
    assert submission_resp.status_code == 201
    submission_data = submission_resp.json()
    assert submission_data["problem_id"] == problem_id
    assert submission_data["status"] == "PENDING"

    list_submissions_resp = client.get(
        "/api/submissions",
        headers=headers,
    )
    assert list_submissions_resp.status_code == 200
    submissions_data = list_submissions_resp.json()
    assert submissions_data["total"] == 1
    assert submissions_data["items"][0]["id"] == submission_data["id"]

    get_submission_resp = client.get(
        f"/api/submissions/{submission_data['id']}",
        headers=headers,
    )
    assert get_submission_resp.status_code == 200
    assert get_submission_resp.json()["id"] == submission_data["id"]
