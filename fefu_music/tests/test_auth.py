import secrets

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status

from fefu_music.db.dao.user_dao import UserDAO
from fefu_music.services.github.schema import GithubUser


@pytest.mark.anyio
async def test_auth_existing_user(
    client: AsyncClient,
    fastapi_app: FastAPI,
    mock_github_user: GithubUser,
) -> None:
    """
    Test function to check if an access token is returned when the user exists.

    This function creates a user with the provided GitHub user details, sends a POST
    request to the request_access_token endpoint, and asserts that the response
    status code is 200 and the response contains an access token.

    :param client: The HTTP client.
    :param fastapi_app: The FastAPI application.
    :param mock_github_user: The mocked GitHub user.
    """
    user_dao = UserDAO()
    url = fastapi_app.url_path_for("request_access_token")
    await user_dao.create(
        avatar_url=str(mock_github_user.avatar_url),
        email=mock_github_user.email,  # type: ignore
        name=mock_github_user.name,  # type: ignore
    )

    response = await client.post(url, json={"code": secrets.token_hex(20)})
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()


@pytest.mark.anyio
async def test_auth_not_existing_user(
    client: AsyncClient,
    fastapi_app: FastAPI,
    mock_github_user: GithubUser,
) -> None:
    """
    Test function to check if an access token is returned when the user does not exist.

    This function sends a POST request to the request_access_token endpoint and
    asserts that the response status code is 200 and the response contains an access
    token.

    :param client: The HTTP client.
    :param fastapi_app: The FastAPI application.
    :param mock_github_user: The mocked GitHub user.
    """
    url = fastapi_app.url_path_for("request_access_token")
    response = await client.post(url, json={"code": secrets.token_hex(20)})
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()


@pytest.mark.anyio
async def test_auth_github_no_email(
    client: AsyncClient,
    fastapi_app: FastAPI,
    mock_github_user: GithubUser,
) -> None:
    """
    Test function to check if an error is returned when the GitHub user email is None.

    This function sets the email of the mocked GitHub user to None, sends a POST
    request to the request_access_token endpoint, and asserts that the response
    status code is 400 and the response contains a detail.

    :param client: The HTTP client.
    :param fastapi_app: The FastAPI application.
    :param mock_github_user: The mocked GitHub user.
    """
    url = fastapi_app.url_path_for("request_access_token")
    mock_github_user.email = None
    response = await client.post(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "detail" in response.json()
