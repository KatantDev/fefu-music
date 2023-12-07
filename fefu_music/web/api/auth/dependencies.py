from fastapi import Depends, HTTPException, status

from fefu_music.db.dao.refresh_token_dao import RefreshTokenDAO
from fefu_music.db.models.refresh_token_model import RefreshTokenModel
from fefu_music.services.auth.utils import refresh_security


async def validate_refresh_token(
    refresh_token: str = Depends(refresh_security),
    refresh_token_dao: RefreshTokenDAO = Depends(),
) -> RefreshTokenModel:
    """
    Asynchronous function to validate a refresh token.

    This function uses the refresh token provided as a parameter to fetch the
    corresponding RefreshTokenModel from the database. If the refresh token does not
    exist in the database, an HTTPException is raised with status code 401.

    :param refresh_token: The refresh token obtained from the cookies.
    :param refresh_token_dao: The RefreshToken Data Access Object (DAO)
                              used to interact with the database.
    :return: A RefreshTokenModel object corresponding to the provided refresh token.
    :raises HTTPException: If the refresh token does not exist in the database,
                           an HTTPException is raised with status code 401.
    """
    refresh_token_model = await refresh_token_dao.get_by_id(
        refresh_token=refresh_token,
    )
    if refresh_token_model is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    return refresh_token_model
