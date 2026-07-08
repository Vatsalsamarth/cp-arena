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

        filters = []

        if title:
            filters.append(Problem.title.ilike(f"%{title}%"))

        if slug:
            filters.append(Problem.slug.ilike(f"%{slug}%"))

        if min_difficulty is not None:
            filters.append(Problem.difficulty >= min_difficulty)

        if max_difficulty is not None:
            filters.append(Problem.difficulty <= max_difficulty)

        stmt = select(Problem)
        count_stmt = select(func.count()).select_from(Problem)

        for condition in filters:
            stmt = stmt.where(condition)
            count_stmt = count_stmt.where(condition)

        sort_column = {
            "id": Problem.id,
            "difficulty": Problem.difficulty,
            "title": Problem.title,
        }.get(sort_by, Problem.id)

        if order == "desc":
            primary_order = sort_column.desc()
            secondary_order = Problem.id.desc()
        else:
            primary_order = sort_column.asc()
            secondary_order = Problem.id.asc()

        if sort_column == Problem.id:
            stmt = stmt.order_by(primary_order)
        else:
            stmt = stmt.order_by(primary_order, secondary_order)

        paginated_stmt = stmt.limit(limit + 1).offset(offset)
        rows = list(self.db.scalars(paginated_stmt).all())

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
