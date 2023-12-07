from fastapi import APIRouter, Depends, HTTPException, Response
from starlette import status

from fefu_music.db.dao.refresh_token_dao import RefreshTokenDAO
from fefu_music.db.dao.user_dao import UserDAO
from fefu_music.db.models.refresh_token_model import RefreshTokenModel
from fefu_music.services.auth.schema import TokenDTO, User
from fefu_music.services.auth.utils import create_and_get_access_data
from fefu_music.services.github.dependencies import get_github_user_data
from fefu_music.services.github.schema import GithubUser
from fefu_music.web.api.auth.dependencies import validate_refresh_token

router = APIRouter()


@router.post(
    path="/oauth/token",
    status_code=status.HTTP_200_OK,
    response_model=TokenDTO,
)
async def request_access_token(
    response: Response,
    github_user: GithubUser = Depends(get_github_user_data),
    user_dao: UserDAO = Depends(),
) -> TokenDTO:
    """
    Asynchronous function to request an access token.

    This function uses the GitHub user data to check if the user exists in the database.
    If the user does not exist, a new user is created. Then, an access token is created
    and returned.

    :param response: FastAPI response.
    :param github_user: The GitHub user data obtained from the GitHub API.
    :param user_dao: The User Data Access Object (DAO) used to interact
                     with the database.
    :raises HTTPException: If the GitHub user's email is None,
                           an HTTPException is raised with status code 400.
    :return: A TokenDTO object containing the access token.
    """
    if github_user.email is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email in github profile is required",
        )
    user_model = await user_dao.get_by_email(github_user.email)
    if user_model is None:
        user_model = await user_dao.create(
            name=github_user.name if github_user.name is not None else "Fefu Music",
            email=github_user.email,
            avatar_url=str(github_user.avatar_url),
        )
    user_dto = User.model_validate(user_model)

    access_token = await create_and_get_access_data(
        response=response,
        user_dto=user_dto,
    )
    return TokenDTO(access_token=access_token)


@router.post(
    path="/oauth/token/refresh",
    status_code=status.HTTP_200_OK,
)
async def refresh_token_from_cookies(
    response: Response,
    refresh_token: RefreshTokenModel = Depends(validate_refresh_token),
    refresh_token_dao: RefreshTokenDAO = Depends(),
) -> TokenDTO:
    """
    Asynchronous function to refresh an access token.

    This function uses the refresh token provided in the cookies to generate a new
    access token.
    The old refresh token is deleted from the database, and a new one
    is created and set in the cookies. The function returns the new access token.

    :param response: FastAPI response.
    :param refresh_token: The refresh token obtained from the cookies.
    :param refresh_token_dao: The RefreshToken Data Access Object (DAO)
                              used to interact with the database.
    :return: A TokenDTO object containing the new access token.
    """
    await refresh_token_dao.delete_by_id(refresh_token=refresh_token.id)
    user_dto = User.model_validate(refresh_token.user)

    access_token = await create_and_get_access_data(
        response=response,
        user_dto=user_dto,
    )
    return TokenDTO(access_token=access_token)
