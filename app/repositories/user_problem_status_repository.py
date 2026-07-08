from typing import Any

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
        # Delegate cache invalidation to shared helper to avoid duplicating
        # the tracked-key deletion logic.
        from app.core.cache import invalidate_tracked

        try:
            invalidate_tracked(redis_client, "leaderboard:keys")
        except Exception:
            # Non-fatal: cache invalidation should not break DB writes.
            pass

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
            primary_order = sort_column.desc()
            secondary_order = UserProblemStatus.id.desc()
        else:
            primary_order = sort_column.asc()
            secondary_order = UserProblemStatus.id.asc()

        stmt = (
            select(UserProblemStatus)
            .join(UserProblemStatus.problem)
            .options(selectinload(UserProblemStatus.problem))
            .where(UserProblemStatus.user_id == user_id)
            .order_by(primary_order, secondary_order)
            .limit(limit + 1)
            .offset(offset)
        )

        count_stmt = (
            select(func.count())
            .select_from(UserProblemStatus)
            .where(UserProblemStatus.user_id == user_id)
        )

        rows = list(self.db.scalars(stmt).all())
        has_next = len(rows) > limit
        items = rows[:limit]

        if has_next:
            total = self.db.scalar(count_stmt) or 0
        elif items:
            total = offset + len(items)
        elif offset == 0:
            total = 0
        else:
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
            if order == "desc":
                stmt = base_stmt.order_by(User.username.desc(), User.id.asc())
            else:
                stmt = base_stmt.order_by(User.username.asc(), User.id.asc())
        else:
            score_column = func.count(UserProblemStatus.id)
            if order == "desc":
                stmt = base_stmt.order_by(
                    score_column.desc(),
                    User.username.asc(),
                    User.id.asc(),
                )
            else:
                stmt = base_stmt.order_by(
                    score_column.asc(),
                    User.username.asc(),
                    User.id.asc(),
                )

        stmt = stmt.limit(limit + 1).offset(offset)

        count_stmt = select(
            func.count(func.distinct(UserProblemStatus.user_id))
        ).select_from(UserProblemStatus)

        rows_with_extra = self.db.execute(stmt).all()
        has_next = len(rows_with_extra) > limit
        rows = rows_with_extra[:limit]

        if has_next:
            total = self.db.scalar(count_stmt) or 0
        elif rows:
            total = offset + len(rows)
        elif offset == 0:
            total = 0
        else:
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
