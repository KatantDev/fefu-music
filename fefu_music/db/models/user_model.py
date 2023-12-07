from enum import Enum

from tortoise import fields, models


class UserStatusEnum(str, Enum):  # noqa: WPS600
    """Enum for user status."""

    USER = "user"
    ADMIN = "admin"


class UserModel(models.Model):
    """Model for users."""

    id = fields.UUIDField(pk=True)
    name = fields.TextField()  # noqa: WPS432
    avatar_url = fields.TextField()  # noqa: WPS432
    email = fields.CharField(max_length=320, unique=True)  # noqa: WPS432
    status = fields.CharEnumField(UserStatusEnum, default=UserStatusEnum.USER)
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
