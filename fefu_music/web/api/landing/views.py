from typing import List

from fastapi import APIRouter, Depends, Query
from yandex_music import ClientAsync

from fefu_music.services.yandex_music_api import utils
from fefu_music.services.yandex_music_api.dependencies import get_yandex_music_client
from fefu_music.web.api.landing.schema import AlbumDTO, ArtistShortDTO, TrackShortDTO

router = APIRouter()


@router.get(
    "/charts",
    response_model=List[TrackShortDTO],
)
async def get_chart(
    limit: int = Query(default=10, ge=1, le=100),  # noqa: WPS432
    offset: int = Query(default=0, ge=0, le=100),  # noqa: WPS432
    yandex_music_client: ClientAsync = Depends(get_yandex_music_client),
) -> List[TrackShortDTO]:
    """
    Asynchronous function to get a chart of tracks from Yandex Music.

    This function uses the Yandex Music API to fetch a chart of tracks. The number of
    tracks fetched can be controlled by the 'limit' parameter. The 'offset' parameter
    can be used to skip a certain number of tracks from the start.

    :param limit: The maximum number of tracks to return. Default to 10.
                  Must be between 1 and 100.
    :param offset: The number of tracks to skip from the start. Default to 0.
                   Must be between 0 and 100.
    :param yandex_music_client: An instance of the Yandex Music client.
    :return: A list of track data transfer objects (DTOs).
    """
    chart_info = await yandex_music_client.chart(
        params={"limit": limit} if offset == 0 else {},
    )
    track_dtos = []
    for track in chart_info.chart.tracks[offset : offset + limit]:
        track_short = track.track
        track_dtos.append(
            TrackShortDTO(
                id=track_short.id,
                title=track_short.title,
                artists=[
                    ArtistShortDTO(
                        id=artist.id,
                        name=artist.name,
                    )
                    for artist in track_short.artists
                ],
                duration_ms=track_short.duration_ms,
                duration_text=utils.format_duration(track_short.duration_ms),
                cover_url=track_short.get_cover_url("100x100"),
            ),
        )
    return track_dtos


@router.get(
    path="/new-releases",
    response_model=List[AlbumDTO],
)
async def get_new_releases(
    limit: int = Query(default=10, ge=1, le=50),  # noqa: WPS432
    offset: int = Query(default=0, ge=0, le=50),  # noqa: WPS432
    yandex_music_client: ClientAsync = Depends(get_yandex_music_client),
) -> List[AlbumDTO]:
    """
    Asynchronous function to get new album releases from Yandex Music.

    This function uses the Yandex Music API to fetch new album releases. The number of
    albums fetched can be controlled by the 'limit' parameter. The 'offset' parameter
    can be used to skip a certain number of albums from the start.

    :param limit: The maximum number of albums to return. Default to 10.
                  Must be between 1 and 50.
    :param offset: The number of albums to skip from the start. Default to 0.
                   Must be between 0 and 50.
    :param yandex_music_client: An instance of the Yandex Music client.
    :return: A list of album data transfer objects (DTOs).
    """
    new_releases = await yandex_music_client.new_releases()
    new_releases = new_releases.new_releases[offset : offset + limit]
    album_dtos = []
    for album in await yandex_music_client.albums(new_releases):
        album_dtos.append(
            AlbumDTO(
                id=album.id,
                title=album.title,
                cover_url=album.get_cover_url("400x400"),
                track_count=album.track_count,
            ),
        )
    return album_dtos
