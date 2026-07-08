import json

from sqlalchemy.orm import Session

from app.core.cache import set_tracked
from app.core.redis import redis_client
from app.models.user import User
from app.repositories.user_problem_status_repository import (
    UserProblemStatusRepository,
)
from app.schemas.user_problem_status import (
    LeaderboardEntryResponse,
    LeaderboardListResponse,
    SolvedProblemListResponse,
    SolvedProblemResponse,
)


class UserProblemStatusService:
    """
    Business logic for solved problems and leaderboard data.
    """

    def __init__(self, db: Session):
        self.repository = UserProblemStatusRepository(db)

    def get_solved_problems(
        self,
        *,
        current_user: User,
        limit: int = 20,
        offset: int = 0,
        sort_by: str = "first_solved_at",
        order: str = "desc",
    ) -> SolvedProblemListResponse:
        """
        Return the list of problems solved by the current user.
        """

        statuses, total = self.repository.list_by_user_id(
            user_id=current_user.id,
            limit=limit,
            offset=offset,
            sort_by=sort_by,
            order=order,
        )

        return SolvedProblemListResponse(
            items=[
                SolvedProblemResponse(
                    problem_id=status.problem_id,
                    title=status.problem.title,
                    slug=status.problem.slug,
                    first_solved_at=status.first_solved_at,  # type: ignore[assignment]
                )
                for status in statuses
            ],
            total=total,
            limit=limit,
            offset=offset,
            has_next=offset + limit < total,
        )

    def get_leaderboard(
        self,
        *,
        limit: int = 50,
        offset: int = 0,
        sort_by: str = "solved_count",
        order: str = "desc",
    ) -> LeaderboardListResponse:
        """
        Return leaderboard entries ordered by solved problem count.
        """

        cache_key = f"leaderboard:{sort_by}:{order}:{limit}:{offset}"
        cached = redis_client.get(cache_key)

        if cached is not None:
            payload = json.loads(cached)
            return LeaderboardListResponse(
                items=[
                    LeaderboardEntryResponse(
                        rank=item[0],
                        user_id=item[1],
                        username=item[2],
                        score=item[3],
                    )
                    for item in payload["items"]
                ],
                total=payload["total"],
                limit=payload["limit"],
                offset=payload["offset"],
                has_next=payload["has_next"],
            )

        rows, total = self.repository.list_leaderboard(
            limit=limit,
            offset=offset,
            sort_by=sort_by,
            order=order,
        )

        items = [
            (
                offset + index + 1,
                int(row[0]),
                str(row[1]),
                int(row[2]),
            )
            for index, row in enumerate(rows)
        ]

        payload = {
            "items": items,
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_next": offset + limit < total,
        }

        # Use helper to set the cache and track the key for invalidation.
        set_tracked(
            redis_client=redis_client,
            tracking_set="leaderboard:keys",
            key=cache_key,
            value=json.dumps(payload),
            ex=15,
        )

        return LeaderboardListResponse(
            items=[
                LeaderboardEntryResponse(
                    rank=item[0],
                    user_id=item[1],
                    username=item[2],
                    score=item[3],
                )
                for item in items
            ],
            total=total,
            limit=limit,
            offset=offset,
            has_next=offset + limit < total,
        )
