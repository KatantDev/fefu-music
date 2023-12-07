from typing import Optional

from fefu_music.db.models.user_model import UserModel


class UserDAO:
    """Class for accessing user table."""

    @staticmethod
    async def create(
        name: str,
        email: str,
        avatar_url: str,
    ) -> UserModel:
        """
        Create user with name, email and password.

        :param name: Full name.
        :param email: User email.
        :param avatar_url: Avatar URL.
        :return: User model.
        """
        return await UserModel.create(
            name=name,
            email=email,
            avatar_url=avatar_url,
        )

    @staticmethod
    async def get_by_email(email: str) -> Optional[UserModel]:
        """
        Get user by email if exists.

        :param email: User email.
        :return: User model if exists.
        """
        return await UserModel.get_or_none(email=email)

    @staticmethod
    async def get_by_id(user_id: int) -> UserModel:
        """
        Get user by id.

        :param user_id: User id.
        :return: User model.
        """
        return await UserModel.get(id=user_id)

    @staticmethod
    async def exists_by_email(email: str) -> bool:
        """
        Check if user with email exists.

        :param email: User email.
        :return: True if user exists.
        """
        return await UserModel.exists(email=email)
