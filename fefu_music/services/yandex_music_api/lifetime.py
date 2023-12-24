from fastapi import FastAPI
from ymdantic import YMClient

from fefu_music.settings import settings


def startup(app: FastAPI) -> None:
    """
    Function to initialize the Yandex Music client when the FastAPI application starts.

    This function is called when the FastAPI application starts up. It creates a new
    instance of the Yandex Music client using the Yandex Music token from the
    application settings, and assigns it to the application state.

    :param app: The FastAPI application.
    """
    if settings.yandex_music_token:
        app.state.ym_client = YMClient(token=settings.yandex_music_token)
