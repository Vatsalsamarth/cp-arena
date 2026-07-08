from pydantic import BaseModel, ConfigDict, Field


class ProblemCreate(BaseModel):
    """
    Request schema for creating a problem.
    """

    title: str = Field(
        min_length=3,
        max_length=200,
    )

    slug: str = Field(
        min_length=3,
        max_length=200,
    )

    statement: str = Field(
        min_length=10,
    )

    difficulty: int = Field(
        ge=800,
        le=3500,
    )


class ProblemUpdate(BaseModel):
    """
    Request schema for updating a problem.
    All fields are optional to support partial updates.
    """

    title: str | None = Field(
        default=None,
        min_length=3,
        max_length=200,
    )

    slug: str | None = Field(
        default=None,
        min_length=3,
        max_length=200,
    )

    statement: str | None = Field(
        default=None,
        min_length=10,
    )

    difficulty: int | None = Field(
        default=None,
        ge=800,
        le=3500,
    )


class ProblemResponse(BaseModel):
    """
    Response schema for a problem.
    """

    id: int
    title: str
    slug: str
    statement: str
    difficulty: int

    model_config = ConfigDict(
        from_attributes=True,
    )


class ProblemListResponse(BaseModel):
    """
    Paginated response for problems.
    """

    items: list[ProblemResponse]
    total: int
    limit: int
    offset: int
    has_next: bool
