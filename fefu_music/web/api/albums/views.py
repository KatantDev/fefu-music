from fastapi import APIRouter, Depends
from yandex_music import Album, ClientAsync

from fefu_music.services.yandex_music_api import get_yandex_music_client
from fefu_music.web.api.albums.schema import AlbumDTO

router = APIRouter()


@router.get(
    "/albums/{album_id}",
    response_model=AlbumDTO,
)
async def get_album(
    album_id: int,
    yandex_music_client: ClientAsync = Depends(get_yandex_music_client),
) -> Album:
    """
    Asynchronous function to get an album from Yandex Music.

    This function uses the Yandex Music API to fetch an album by its ID. It fetches
    the album along with its tracks.

    :param album_id: The ID of the album to fetch.
    :param yandex_music_client: An instance of the Yandex Music client.
    :return: An AlbumDTO object containing the album data and its tracks.
    """
    return await yandex_music_client.albums_with_tracks(album_id)
