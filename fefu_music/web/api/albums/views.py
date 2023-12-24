from fastapi import APIRouter, Depends
from ymdantic import YMClient, models

from fefu_music.services.yandex_music_api import get_ymclient
from fefu_music.web.api.albums.schema import AlbumDTO

router = APIRouter()


@router.get(
    "/albums/{album_id}",
    response_model=AlbumDTO,
)
async def get_album(
    album_id: int,
    ym_client: YMClient = Depends(get_ymclient),
) -> models.Album:
    """
    Asynchronous function to get an album from Yandex Music.

    This function uses the Yandex Music API to fetch an album by its ID. It fetches
    the album along with its tracks.

    :param album_id: The ID of the album to fetch.
    :param ym_client: An instance of the Yandex Music client.
    :return: An AlbumDTO object containing the album data and its tracks.
    """
    return await ym_client.get_album_with_tracks(album_id)
