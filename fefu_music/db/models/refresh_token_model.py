import typing
from datetime import datetime

from tortoise import fields, models

from fefu_music.settings import settings

if typing.TYPE_CHECKING:
    from fefu_music.db.models.user_model import UserModel


def expires_at() -> datetime:
    """
    Get expires at datetime.

    :return: Datetime.
    """
    return datetime.utcnow() + settings.refresh_token_expire_timedelta


class RefreshTokenModel(models.Model):
    """Model for refresh tokens."""

    id = fields.UUIDField(pk=True)
    expires_at = fields.DatetimeField(default=expires_at)
    created_at = fields.DatetimeField(auto_now_add=True)

    user: fields.ForeignKeyRelation["UserModel"] = fields.ForeignKeyField(
        model_name="models.UserModel",
    )
