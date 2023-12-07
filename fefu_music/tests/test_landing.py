import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status


@pytest.mark.anyio
async def test_get_chart_count(
    fastapi_app: FastAPI,
    client: AsyncClient,
) -> None:
    """
    Test to verify that the get_chart endpoint returns the expected number of tracks.

    :param fastapi_app: The FastAPI application.
    :param client: The HTTP client.
    """
    url = fastapi_app.url_path_for("get_chart")
    response = await client.get(
        url,
        params={
            "offset": 0,
            "limit": 10,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 10


@pytest.mark.anyio
async def test_get_chart_offset(
    fastapi_app: FastAPI,
    client: AsyncClient,
) -> None:
    """
    Test to verify different tracks are returned with offset.

    :param fastapi_app: The FastAPI application.
    :param client: The HTTP client.
    """
    url = fastapi_app.url_path_for("get_chart")
    response1 = await client.get(
        url,
        params={
            "offset": 0,
            "limit": 10,
        },
    )
    response2 = await client.get(
        url,
        params={
            "offset": 10,
            "limit": 10,
        },
    )
    assert response1.json() != response2.json()


@pytest.mark.anyio
async def test_get_chart_invalid_limit(
    fastapi_app: FastAPI,
    client: AsyncClient,
) -> None:
    """
    Test for error when invalid limit is provided to get_chart.

    :param fastapi_app: The FastAPI application.
    :param client: The HTTP client.
    """
    url = fastapi_app.url_path_for("get_chart")
    response = await client.get(
        url,
        params={
            "offset": 0,
            "limit": -1,
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.anyio
async def test_get_new_releases_count(
    fastapi_app: FastAPI,
    client: AsyncClient,
) -> None:
    """
    Test to verify that the get_new_releases endpoint returns the length of albums.

    :param fastapi_app: The FastAPI application.
    :param client: The HTTP client.
    """
    url = fastapi_app.url_path_for("get_new_releases")
    response = await client.get(
        url,
        params={
            "offset": 0,
            "limit": 10,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 10


@pytest.mark.anyio
async def test_get_new_releases_offset(
    fastapi_app: FastAPI,
    client: AsyncClient,
) -> None:
    """
    Test to verify that the get_new_releases endpoint returns different albums.

    :param fastapi_app: The FastAPI application.
    :param client: The HTTP client.
    """
    url = fastapi_app.url_path_for("get_new_releases")
    response1 = await client.get(
        url,
        params={
            "offset": 0,
            "limit": 10,
        },
    )
    response2 = await client.get(
        url,
        params={
            "offset": 10,
            "limit": 10,
        },
    )
    assert response1.json() != response2.json()


@pytest.mark.anyio
async def test_get_new_releases_invalid_limit(
    fastapi_app: FastAPI,
    client: AsyncClient,
) -> None:
    """
    Test for error when invalid limit is provided to get_new_releases.

    :param fastapi_app: The FastAPI application.
    :param client: The HTTP client.
    """
    url = fastapi_app.url_path_for("get_new_releases")
    response = await client.get(
        url,
        params={
            "offset": 0,
            "limit": -1,
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
