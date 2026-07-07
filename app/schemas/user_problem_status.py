from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SolvedProblemResponse(BaseModel):
    """
    Representation of a solved problem for the current user.
    """

    model_config = ConfigDict(from_attributes=True)

    problem_id: int
    title: str
    slug: str
    first_solved_at: datetime


class SolvedProblemListResponse(BaseModel):
    """
    Paginated response for solved problems.
    """

    items: list[SolvedProblemResponse]
    total: int
    limit: int
    offset: int
    has_next: bool


class LeaderboardEntryResponse(BaseModel):
    """
    Representation of a leaderboard entry.
    """

    model_config = ConfigDict(from_attributes=True)

    rank: int
    user_id: int
    username: str
    score: int


class LeaderboardListResponse(BaseModel):
    """
    Paginated response for leaderboard entries.
    """

    items: list[LeaderboardEntryResponse]
    total: int
    limit: int
    offset: int
    has_next: bool
