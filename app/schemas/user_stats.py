from pydantic import BaseModel


class UserStatsResponse(BaseModel):
    """
    User submission statistics.
    """

    total_submissions: int
    accepted: int
    wrong_answer: int
    runtime_error: int
    compilation_error: int
    acceptance_rate: float