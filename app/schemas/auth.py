from pydantic import BaseModel, ConfigDict, Field


class LoginRequest(BaseModel):
    """
    Request body for user authentication.
    """

    username: str = Field(
        min_length=3,
        max_length=50,
    )

    password: str = Field(
        min_length=8,
    )


class TokenResponse(BaseModel):
    """
    Response returned after successful authentication.
    """

    access_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(
        from_attributes=True,
    )