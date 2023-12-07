from datetime import datetime
from typing import Any, AsyncGenerator
from unittest.mock import Mock
from uuid import uuid4

import nest_asyncio
import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from tortoise import Tortoise
from tortoise.contrib.test import finalizer, initializer

from fefu_music.db.config import MODELS_MODULES, TORTOISE_CONFIG
from fefu_music.db.dao.refresh_token_dao import RefreshTokenDAO
from fefu_music.db.dao.user_dao import UserDAO
from fefu_music.db.models.user_model import UserModel
from fefu_music.services import yandex_music_api
from fefu_music.services.github.dependencies import get_github_user_data
from fefu_music.services.github.schema import GithubUser
from fefu_music.settings import settings
from fefu_music.web.application import get_app

nest_asyncio.apply()


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """
    Backend for anyio pytest plugin.

    :return: backend name.
    """
    return "asyncio"


@pytest.fixture(autouse=True)
async def initialize_db() -> AsyncGenerator[None, None]:
    """
    Initialize models and database.

    :yields: Nothing.
    """
    initializer(
        MODELS_MODULES,
        db_url=str(settings.db_url),
        app_label="models",
    )
    await Tortoise.init(config=TORTOISE_CONFIG)

    yield

    await Tortoise.close_connections()
    finalizer()


@pytest.fixture
def fastapi_app() -> FastAPI:
    """
    Fixture for creating FastAPI app.

    :return: fastapi app with mocked dependencies.
    """
    application = get_app()
    return application  # noqa: WPS331


@pytest.fixture(autouse=True)
async def initialize_yandex_music_client(
    fastapi_app: FastAPI,
) -> AsyncGenerator[None, None]:
    """
    Initialize a Yandex Music client.

    :param fastapi_app: Current FastAPI application.
    :yields: Nothing
    """
    yandex_music_api.startup(app=fastapi_app)
    yield


@pytest.fixture
async def client(
    fastapi_app: FastAPI,
    anyio_backend: Any,
) -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture that creates client for requesting server.

    :param fastapi_app: The application.
    :param anyio_backend: The backend for anyio.
    :yield: a client for the app.
    """
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def mock_github_user(
    fastapi_app: FastAPI,
) -> GithubUser:
    """
    Fixture for creating a mock GithubUser.

    :return: A mock GithubUser object.
    """
    mock_user = Mock(spec=GithubUser)
    mock_user.email = "test@example.com"
    mock_user.name = "Test User"
    mock_user.avatar_url = "http://example.com/avatar.png"
    fastapi_app.dependency_overrides[get_github_user_data] = lambda: mock_user
    return mock_user


@pytest.fixture
def mock_user_model(
    fastapi_app: FastAPI,
) -> GithubUser:
    """
    Fixture for creating a mock UserModel.

    :return: A mock UserModel object.
    """
    mock_user = Mock(spec=UserModel)
    mock_user.id = uuid4()
    mock_user.email = "test@example.com"
    mock_user.name = "Test User"
    mock_user.avatar_url = "http://example.com/avatar.png"
    mock_user.status = "user"
    mock_user.created_at = datetime.now()
    return mock_user


@pytest.fixture
def mock_refresh_token_dao(
    fastapi_app: FastAPI,
) -> RefreshTokenDAO:
    """
    Fixture for creating a mock RefreshTokenDAO.

    :return: A mock RefreshTokenDAO object.
    """
    mock_refresh_token_dao = Mock(spec=RefreshTokenDAO)
    fastapi_app.dependency_overrides[RefreshTokenDAO] = lambda: mock_refresh_token_dao
    return mock_refresh_token_dao


@pytest.fixture
def mock_user_dao(
    fastapi_app: FastAPI,
) -> UserDAO:
    """
    Fixture for creating a mock UserDAO.

    :return: A mock UserDAO object.
    """
    mock_user_dao = Mock(spec=UserDAO)
    fastapi_app.dependency_overrides[UserDAO] = lambda: mock_user_dao
    return mock_user_dao
