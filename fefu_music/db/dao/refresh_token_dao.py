from datetime import datetime
from typing import Optional, Union
from uuid import UUID

from tortoise.expressions import Subquery

from fefu_music.db.models.refresh_token_model import RefreshTokenModel


class RefreshTokenDAO:
    """Class for accessing refresh token table."""

    @staticmethod
    async def create(
        user_id: UUID,
    ) -> RefreshTokenModel:
        """
        Create refresh token model.

        :param user_id: User id.
        :return: Refresh token model.
        """
        return await RefreshTokenModel.create(
            user_id=user_id,
        )

    @staticmethod
    async def delete_old_when_limit(
        user_id: UUID,
    ) -> None:
        """
        Delete old refresh tokens by user.

        :param user_id: User id.
        """
        subquery = Subquery(
            RefreshTokenModel.filter(user_id=user_id)
            .order_by("-created_at")
            .offset(4)
            .values("id"),
        )
        await RefreshTokenModel.filter(id__in=subquery).delete()

    @staticmethod
    async def get_by_id(
        refresh_token: str,
    ) -> Optional[RefreshTokenModel]:
        """
        Check the existence of refresh token.

        :param refresh_token: Refresh token id.
        :return: True if refresh token exists.
        """
        return await RefreshTokenModel.get_or_none(
            id=refresh_token,
            expires_at__gte=datetime.utcnow(),
        ).prefetch_related("user")

    @staticmethod
    async def delete_by_id(refresh_token: Union[str, UUID]) -> None:
        """
        Delete refresh token by id.

        :param refresh_token: Refresh token id.
        """
        await RefreshTokenModel.filter(id=refresh_token).delete()
