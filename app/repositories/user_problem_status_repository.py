from typing import Any

import json

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.core.redis import redis_client
from app.models.problem import Problem
from app.models.user import User
from app.models.user_problem_status import UserProblemStatus


class UserProblemStatusRepository:
    """
    Handles all database operations for user problem solve status.
    """

    def __init__(self, db: Session):
        self.db = db

    def _invalidate_leaderboard_cache(self) -> None:
        for key in redis_client.scan_iter(match="leaderboard:*"):
            redis_client.delete(key)

    def get_by_user_and_problem(
        self,
        *,
        user_id: int,
        problem_id: int,
    ) -> UserProblemStatus | None:
        """
        Return a UserProblemStatus record for a specific user and problem.
        """

        stmt = select(UserProblemStatus).where(
            UserProblemStatus.user_id == user_id,
            UserProblemStatus.problem_id == problem_id,
        )

        return self.db.scalar(stmt)

    def list_by_user_id(
        self,
        *,
        user_id: int,
        limit: int = 20,
        offset: int = 0,
        sort_by: str = "first_solved_at",
        order: str = "desc",
    ) -> tuple[list[UserProblemStatus], int]:
        """
        Return solved problems for a specific user with pagination and sorting.
        """

        sort_columns: dict[str, Any] = {
            "first_solved_at": UserProblemStatus.first_solved_at,
            "problem_title": Problem.title,
        }

        sort_column = sort_columns.get(
            sort_by,
            UserProblemStatus.first_solved_at,
        )

        if order == "desc":
            sort_column = sort_column.desc()
        else:
            sort_column = sort_column.asc()

        stmt = (
            select(UserProblemStatus)
            .join(UserProblemStatus.problem)
            .options(selectinload(UserProblemStatus.problem))
            .where(UserProblemStatus.user_id == user_id)
            .order_by(sort_column)
            .limit(limit)
            .offset(offset)
        )

        count_stmt = (
            select(func.count())
            .select_from(UserProblemStatus)
            .where(UserProblemStatus.user_id == user_id)
        )

        items = list(self.db.scalars(stmt).all())
        total = self.db.scalar(count_stmt) or 0

        return items, total

    def list_leaderboard(
        self,
        *,
        limit: int = 50,
        offset: int = 0,
        sort_by: str = "solved_count",
        order: str = "desc",
    ) -> tuple[list[tuple[int, str, int]], int]:
        """
        Return leaderboard rows ordered by solved count.
        """

        base_stmt = (
            select(
                User.id.label("user_id"),
                User.username,
                func.count(UserProblemStatus.id).label("solved_count"),
            )
            .join(User, UserProblemStatus.user_id == User.id)
            .group_by(User.id, User.username)
        )

        if sort_by == "username":
            order_column = User.username
        else:
            order_column = func.count(UserProblemStatus.id)

        if order == "desc":
            order_column = order_column.desc()
        else:
            order_column = order_column.asc()

        stmt = base_stmt.order_by(order_column, User.username.asc()).limit(limit).offset(offset)

        count_stmt = (
            select(func.count(func.distinct(UserProblemStatus.user_id)))
            .select_from(UserProblemStatus)
        )

        rows = self.db.execute(stmt).all()
        total = self.db.scalar(count_stmt) or 0

        return [
            (
                int(row.user_id),
                str(row.username),
                int(row.solved_count),
            )
            for row in rows
        ], total

    def create(
        self,
        *,
        user_id: int,
        problem_id: int,
    ) -> UserProblemStatus:
        """
        Create a new UserProblemStatus record.
        """

        status = UserProblemStatus(
            user_id=user_id,
            problem_id=problem_id,
        )

        self.db.add(status)
        self.db.commit()
        self.db.refresh(status)
        self._invalidate_leaderboard_cache()

        return status

    def create_if_missing(
        self,
        *,
        user_id: int,
        problem_id: int,
    ) -> UserProblemStatus | None:
        """
        Create the status record only when it does not already exist.
        """

        existing_status = self.get_by_user_and_problem(
            user_id=user_id,
            problem_id=problem_id,
        )

        if existing_status is not None:
            return existing_status

        return self.create(
            user_id=user_id,
            problem_id=problem_id,
        )
