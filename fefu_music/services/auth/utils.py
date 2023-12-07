from datetime import timedelta

from fastapi import HTTPException, Response, Security
from fastapi_jwt import JwtAccessBearer, JwtAuthorizationCredentials
from passlib.context import CryptContext
from starlette import status

from fefu_music.db.dao.refresh_token_dao import RefreshTokenDAO
from fefu_music.services.auth.schema import RefreshCookie, User
from fefu_music.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
access_security = JwtAccessBearer(
    secret_key=settings.secret_key,
    auto_error=False,
    access_expires_delta=timedelta(seconds=10),
)
refresh_security = RefreshCookie(
    refresh_token_expire_timedelta=settings.refresh_token_expire_timedelta,
)


def validate_access_security(
    credentials: JwtAuthorizationCredentials = Security(access_security),
) -> JwtAuthorizationCredentials:
    """
    Function to validate access security.

    This function checks if the credentials from the access token are valid. If the
    credentials are not valid, it raises an HTTPException with a status code of
    401 (Unauthorized).

    :param credentials: The credentials from the access token.
    :raises HTTPException: If the credentials are invalid.
    :return: The credentials if they are valid.
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    return credentials


async def create_and_get_access_data(
    response: Response,
    user_dto: User,
) -> str:
    """
    Asynchronous function to create and set a refresh token.

    This function creates a new refresh token for the specified user and sets it in
    the response. It also creates an access token with the user's ID and any
    additional data provided.

    :param response: The response object to set the refresh token in.
    :param user_dto: The user to create the refresh token for.
    :return: The created access token.
    """
    refresh_token_dao = RefreshTokenDAO()
    await refresh_token_dao.delete_old_when_limit(user_id=user_dto.id)

    access_token = access_security.create_access_token(
        subject=user_dto.model_dump(mode="json"),
    )
    refresh_token = await refresh_token_dao.create(user_id=user_dto.id)

    refresh_security.set_refresh_cookie(response, refresh_token.id)
    return access_token


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Function to verify a password.

    This function checks if a plain text password matches a hashed password using the
    bcrypt password hashing algorithm.

    :param plain_password: The plain text password to check.
    :param hashed_password: The hashed password to check against.
    :return: True if the password is correct, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Function to get a password hash.

    This function hashes a plain text password using the bcrypt password hashing
    algorithm.

    :param password: The plain text password to hash.
    :return: The hashed password.
    """
    return pwd_context.hash(password)
