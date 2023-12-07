from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Union

from fastapi import Response
from fastapi.security import APIKeyCookie
from pydantic import UUID4, BaseModel, ConfigDict

from fefu_music.db.models.user_model import UserStatusEnum


class TokenDTO(BaseModel):
    """DTO for token."""

    access_token: str


class GithubOAuthResponse(BaseModel):
    """DTO for GitHub oauth response."""

    access_token: str
    token_type: str
    scope: str


class User(BaseModel):
    """DTO for user."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    name: str
    email: str
    avatar_url: str
    created_at: datetime
    status: UserStatusEnum


class RefreshDeletionEnum(Enum):
    """Enum for refresh deletion."""

    ALL = "all"
    BY_LIMIT = "by_limit"


class RefreshCookie(APIKeyCookie):
    """Custom refresh cookie class."""

    def __init__(
        self,
        refresh_token_expire_timedelta: timedelta,
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(*args, name="refresh_token_cookie", auto_error=False, **kwargs)
        self.refresh_token_expire_timedelta: timedelta = refresh_token_expire_timedelta

    def set_refresh_cookie(
        self,
        response: Response,
        refresh_token: Union[str, UUID4],
    ) -> None:
        """
        Set refresh cookie.

        :param response: Response.
        :param refresh_token: Refresh token.
        """
        seconds_expires = int(self.refresh_token_expire_timedelta.total_seconds())
        response.set_cookie(
            key="refresh_token_cookie",
            value=str(refresh_token),
            httponly=True,
            max_age=seconds_expires,
            path="/api/oauth/token/refresh",
            domain="192.168.0.105",
        )
