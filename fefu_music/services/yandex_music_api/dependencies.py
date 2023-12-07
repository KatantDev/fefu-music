import yandex_music
from fastapi import Request


async def get_yandex_music_client(request: Request) -> yandex_music.ClientAsync:
    """
    Asynchronous function to get the Yandex Music client from the application state.

    This function retrieves the Yandex Music client stored in the application state
    during startup. The client is retrieved from the state of the FastAPI application
    that is handling the current request.

    :param request: The request object associated with the current HTTP request.
    :return: The Yandex Music client stored in the application state.
    """
    return request.app.state.yandex_music_client
