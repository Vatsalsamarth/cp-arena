from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TestCaseCreate(BaseModel):
    """
    Request schema for creating a test case.
    """

    input_data: str = Field(
        min_length=1,
    )

    expected_output: str = Field(
        min_length=1,
    )

    is_sample: bool = False


class TestCaseResponse(BaseModel):
    """
    Response schema for a test case.
    """

    id: int
    problem_id: int
    input_data: str
    expected_output: str
    is_sample: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class TestCaseListResponse(BaseModel):
    """
    Response schema for multiple test cases.
    """

    items: list[TestCaseResponse]
    total: int