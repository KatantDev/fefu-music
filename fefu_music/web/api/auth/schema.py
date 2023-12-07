from pydantic import BaseModel, Field


class OAuthInputDTO(BaseModel):
    """DTO for OAuth input."""

    code: str = Field(min_length=20, max_length=20)  # noqa: WPS432
