from typing import Any, Dict, List

import aiohttp
from fastapi import Body, Depends, HTTPException
from pydantic import ValidationError
from starlette import status

from fefu_music.services.auth.schema import GithubOAuthResponse
from fefu_music.services.github.schema import GithubUser, PrivateUser, PublicUser
from fefu_music.settings import settings


async def get_github_access_token(
    code: str = Body(embed=True),
) -> GithubOAuthResponse:
    """
    Asynchronous function to get a GitHub access token.

    This function sends a POST request to GitHub's OAuth access token endpoint with
    the necessary data to exchange a temporary code for an access token. The function
    is asynchronous and uses aiohttp's ClientSession to send the request.

    :param code: The temporary code received as a response to the
                 OAuth authorization request.
    :raises HTTPException: If the response does not contain an access token.
    :return: The response text from the POST request,
             which should contain the access token.
    """
    url = "https://github.com/login/oauth/access_token"
    headers = {
        "Accept": "application/json",
    }
    data = {
        "client_id": settings.github_client_id,
        "client_secret": settings.github_client_secret,
        "code": code,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data, headers=headers) as response:
            try:
                return GithubOAuthResponse(**(await response.json()))
            except ValidationError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid github temporary code",
                )


async def get_github_user_data(
    github_oauth_response: GithubOAuthResponse = Depends(get_github_access_token),
) -> GithubUser:
    """
    Asynchronous function to get a GitHub user's data.

    This function sends a GET request to GitHub's user endpoint with
    the necessary headers including the access token. The function
    is asynchronous and uses aiohttp's ClientSession to send the request.

    :param github_oauth_response: The response from the OAuth access token request.
    :return: A GithubUser object which can be either a PrivateUser or PublicUser.
    :raises HTTPException: If the response status is not 200, an HTTPException
                           is raised with status code 401.
    """
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {github_oauth_response.access_token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        emails = await get_github_user_emails(session=session)
        async with session.get(
            url="https://api.github.com/user",
        ) as user_response:
            if user_response.status != 200:  # noqa: WPS432
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated to GitHub",
                )

            user_data = await user_response.json()
            user_data.pop("email", None)
            if "business_plus" in user_data:
                return PrivateUser(email=emails[0]["email"], **user_data)
            return PublicUser(email=emails[0]["email"], **user_data)


async def get_github_user_emails(
    session: aiohttp.ClientSession,
) -> List[Dict[str, Any]]:
    """
    Asynchronous function to get a GitHub user's emails.

    This function sends a GET request to GitHub's user emails endpoint with
    the necessary headers including the access token. The function
    is asynchronous and uses aiohttp's ClientSession to send the request.

    :param session: The aiohttp ClientSession to use for the request.
    :return: A list of dictionaries, each representing an email associated
             with the user.
    """
    async with session.get(
        url="https://api.github.com/user/emails",
    ) as email_response:
        # TODO: Rewrite
        return await email_response.json()
