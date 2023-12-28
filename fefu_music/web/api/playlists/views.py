from fastapi import APIRouter, Depends
from ymdantic import YMClient, models

from fefu_music.services.yandex_music_api import get_ymclient
from fefu_music.web.api.playlists.schema import PlaylistDTO

router = APIRouter()


@router.get(
    "/users/{user_id}/playlists/{kind}",
    response_model=PlaylistDTO,
)
async def get_playlist(
    user_id: int,
    kind: int,
    yandex_music_client: YMClient = Depends(get_ymclient),
) -> models.Playlist:
    """
    Asynchronous function to get a playlist from Yandex Music.

    This function uses the Yandex Music API to fetch a playlist by its kind and user ID.

    :param user_id: The ID of the user.
    :param kind: The kind of the playlist.
    :param yandex_music_client: An instance of the Yandex Music client.
    :return: A Playlist object containing the playlist data.
    """
    return await yandex_music_client.get_playlist(
        user_id=user_id,
        playlist_id=kind,
    )
