from typing import Awaitable, Callable

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from ymdantic.exceptions import YandexMusicError

from fefu_music.services import yandex_music_api
from fefu_music.tkq import broker


def register_exception_handler(
    app: FastAPI,
) -> Callable[[Request, YandexMusicError], Awaitable[JSONResponse]]:  # pragma: no cover
    """
    Register exception handler for the application.

    :param app: The fastAPI application.
    :return: Function that actually performs actions.
    """

    @app.exception_handler(YandexMusicError)
    async def _yandex_music_exception_handler(  # noqa: WPS430
        _: Request,
        exc: YandexMusicError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc)},
        )

    return _yandex_music_exception_handler


def register_startup_event(
    app: FastAPI,
) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application startup.

    This function uses fastAPI app to store data
    in the state, such as db_engine.

    :param app: The fastAPI application.
    :return: Function that actually performs actions.
    """

    @app.on_event("startup")
    async def _startup() -> None:  # noqa: WPS430
        app.middleware_stack = None
        if not broker.is_worker_process:
            await broker.startup()
        yandex_music_api.startup(app=app)
        app.middleware_stack = app.build_middleware_stack()
        pass  # noqa: WPS420

    return _startup


def register_shutdown_event(
    app: FastAPI,
) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application's shutdown.

    :param app: fastAPI application.
    :return: Function that actually performs actions.
    """

    @app.on_event("shutdown")
    async def _shutdown() -> None:  # noqa: WPS430
        if not broker.is_worker_process:
            await broker.shutdown()
        pass  # noqa: WPS420

    return _shutdown
