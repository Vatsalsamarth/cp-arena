from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.submission import SubmissionStatus


class SubmissionCreate(BaseModel):
    """
    Request schema for creating a submission.
    """

    problem_id: int = Field(
        gt=0,
    )

    language: str = Field(
        min_length=1,
        max_length=50,
    )

    source_code: str = Field(
        min_length=1,
    )


class SubmissionResponse(BaseModel):
    """
    Response schema for a submission.
    """

    id: int
    user_id: int
    problem_id: int
    language: str
    source_code: str
    status: SubmissionStatus
    execution_time_ms: int | None
    memory_kb: int | None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class SubmissionListResponse(BaseModel):
    """
    Paginated response for submissions.
    """

    items: list[SubmissionResponse]
    total: int
    limit: int
    offset: int
    has_next: bool


class SubmissionFilters(BaseModel):
    """
    Internal filter object used by the service and repository.
    """

    status: SubmissionStatus | None = None
    problem_id: int | None = Field(
        default=None,
        gt=0,
    )
    user_id: int | None = Field(
        default=None,
        gt=0,
    )
    limit: int = Field(
        default=20,
        ge=1,
        le=100,
    )
    offset: int = Field(
        default=0,
        ge=0,
    )