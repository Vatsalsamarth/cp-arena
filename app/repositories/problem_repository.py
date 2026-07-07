from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.problem import Problem


class ProblemRepository:
    """
    Handles all database operations for problems.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        *,
        title: str,
        slug: str,
        statement: str,
        difficulty: int,
    ) -> Problem:
        problem = Problem(
            title=title,
            slug=slug,
            statement=statement,
            difficulty=difficulty,
        )

        self.db.add(problem)
        self.db.commit()
        self.db.refresh(problem)

        return problem

    def get_by_id(self, problem_id: int) -> Problem | None:
        stmt = select(Problem).where(Problem.id == problem_id)
        return self.db.scalar(stmt)

    def get_by_slug(self, slug: str) -> Problem | None:
        stmt = select(Problem).where(Problem.slug == slug)
        return self.db.scalar(stmt)

    def get_by_title(self, title: str) -> Problem | None:
        stmt = select(Problem).where(Problem.title == title)
        return self.db.scalar(stmt)

    def list_all(
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
    ) -> tuple[list[Problem], int]:
        """
        Return a filtered, sorted and paginated list of problems
        together with the total number of matching problems.
        """

        stmt = select(Problem)
        count_stmt = select(func.count()).select_from(Problem)

        if title:
            condition = Problem.title.ilike(f"%{title}%")
            stmt = stmt.where(condition)
            count_stmt = count_stmt.where(condition)

        if slug:
            condition = Problem.slug.ilike(f"%{slug}%")
            stmt = stmt.where(condition)
            count_stmt = count_stmt.where(condition)

        if min_difficulty is not None:
            condition = Problem.difficulty >= min_difficulty
            stmt = stmt.where(condition)
            count_stmt = count_stmt.where(condition)

        if max_difficulty is not None:
            condition = Problem.difficulty <= max_difficulty
            stmt = stmt.where(condition)
            count_stmt = count_stmt.where(condition)

        sort_column = {
            "id": Problem.id,
            "difficulty": Problem.difficulty,
            "title": Problem.title,
        }.get(sort_by, Problem.id)

        if order == "desc":
            stmt = stmt.order_by(sort_column.desc())
        else:
            stmt = stmt.order_by(sort_column.asc())

        stmt = stmt.limit(limit).offset(offset)

        items = list(self.db.scalars(stmt).all())
        total = self.db.scalar(count_stmt) or 0

        return items, total

    def update(self, problem: Problem) -> Problem:
        """
        Persist changes to an existing problem.
        """

        self.db.commit()
        self.db.refresh(problem)

        return problem

    def delete(self, problem: Problem) -> None:
        """
        Delete an existing problem.
        """

        self.db.delete(problem)
        self.db.commit()