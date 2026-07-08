import json

from sqlalchemy.orm import Session

from app.core.cache import invalidate_tracked, set_tracked
from app.core.exceptions import (
    ProblemAlreadyExistsError,
    ProblemNotFoundError,
)
from app.core.redis import redis_client
from app.models.problem import Problem
from app.repositories.problem_repository import ProblemRepository
from app.schemas.problem import ProblemCreate, ProblemUpdate


class ProblemService:
    """
    Contains business logic related to problems.
    """

    def __init__(self, db: Session):
        self.repository = ProblemRepository(db)

    def create_problem(
        self,
        problem_create: ProblemCreate,
    ) -> Problem:
        """
        Create a new problem.
        """

        if self.repository.get_by_title(problem_create.title):
            raise ProblemAlreadyExistsError("Problem title already exists.")

        if self.repository.get_by_slug(problem_create.slug):
            raise ProblemAlreadyExistsError("Problem slug already exists.")

        result = self.repository.create(
            title=problem_create.title,
            slug=problem_create.slug,
            statement=problem_create.statement,
            difficulty=problem_create.difficulty,
        )

        # Invalidate cached problem lists after creating a new problem.
        try:
            invalidate_tracked(redis_client, "problems:keys")
        except Exception:
            pass

        return result

    def list_problems(
        self,
        *,
        title: str | None,
        slug: str | None,
        min_difficulty: int | None,
        max_difficulty: int | None,
        sort_by: str,
        order: str,
        limit: int,
        offset: int,
    ) -> dict:
        """
        Return filtered, sorted and paginated problems together
        with pagination metadata.
        """

        cache_key = (
            f"problems:{title}:{slug}:{min_difficulty}:"
            f"{max_difficulty}:{sort_by}:{order}:{limit}:{offset}"
        )

        cached = redis_client.get(cache_key)

        if cached is not None:
            return json.loads(cached)

        items, total = self.repository.list_all(
            title=title,
            slug=slug,
            min_difficulty=min_difficulty,
            max_difficulty=max_difficulty,
            sort_by=sort_by,
            order=order,
            limit=limit,
            offset=offset,
        )

        # Convert ORM objects into serializable dicts for caching.
        items_payload = [
            {
                "id": p.id,
                "title": p.title,
                "slug": p.slug,
                "statement": p.statement,
                "difficulty": p.difficulty,
            }
            for p in items
        ]

        payload = {
            "items": items_payload,
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_next": offset + limit < total,
        }

        set_tracked(
            redis_client=redis_client,
            tracking_set="problems:keys",
            key=cache_key,
            value=json.dumps(payload),
            ex=30,
        )

        return payload

    def get_problem_or_raise(
        self,
        slug: str,
    ) -> Problem:
        """
        Retrieve a problem by slug or raise an exception.
        """

        problem = self.repository.get_by_slug(slug)

        if problem is None:
            raise ProblemNotFoundError("Problem not found.")

        return problem

    def get_problem_by_slug(
        self,
        slug: str,
    ) -> Problem | None:
        """
        Retrieve a problem by its slug.
        """

        return self.repository.get_by_slug(slug)

    def update_problem(
        self,
        slug: str,
        problem_update: ProblemUpdate,
    ) -> Problem:
        """
        Update an existing problem.
        """

        problem = self.get_problem_or_raise(slug)

        update_data = problem_update.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )

        if "title" in update_data and update_data["title"] != problem.title:
            existing = self.repository.get_by_title(update_data["title"])

            if existing is not None:
                raise ProblemAlreadyExistsError("Problem title already exists.")

        if "slug" in update_data and update_data["slug"] != problem.slug:
            existing = self.repository.get_by_slug(update_data["slug"])

            if existing is not None:
                raise ProblemAlreadyExistsError("Problem slug already exists.")

        for field, value in update_data.items():
            setattr(problem, field, value)

        updated = self.repository.update(problem)

        try:
            invalidate_tracked(redis_client, "problems:keys")
        except Exception:
            pass

        return updated

    def delete_problem(
        self,
        slug: str,
    ) -> None:
        """
        Delete an existing problem.
        """

        problem = self.get_problem_or_raise(slug)

        self.repository.delete(problem)

        try:
            invalidate_tracked(redis_client, "problems:keys")
        except Exception:
            pass
