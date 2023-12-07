import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status


@pytest.mark.anyio
async def test_health(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    Asynchronous test function to check the health of the application.

    This function sends a GET request to the health_check endpoint and asserts that the
    response status code is 200.

    :param client: The HTTP client.
    :param fastapi_app: The FastAPI application.
    """
    url = fastapi_app.url_path_for("health_check")
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK
