from typing import List

from fastapi import APIRouter, Depends, Query
from ymdantic import YMClient, models

from fefu_music.services.yandex_music_api.dependencies import get_ymclient
from fefu_music.web.api.landing.schema import NewReleaseDTO
from fefu_music.web.api.schema import TrackShortDTO

router = APIRouter()


@router.get(
    "/charts",
    response_model=List[TrackShortDTO],
)
async def get_chart(
    limit: int = Query(default=10, ge=1, le=100),  # noqa: WPS432
    offset: int = Query(default=0, ge=0, le=100),  # noqa: WPS432
    yandex_music_client: YMClient = Depends(get_ymclient),
) -> List[models.TrackType]:
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
    chart_info = await yandex_music_client.get_chart(
        limit=limit if offset == 0 else None,
    )
    return [track.track for track in chart_info.chart.tracks[offset : offset + limit]]


@router.get(
    path="/new-releases",
    response_model=List[NewReleaseDTO],
    response_model_exclude_none=True,
)
async def get_new_releases(
    limit: int = Query(default=10, ge=1, le=50),  # noqa: WPS432
    offset: int = Query(default=0, ge=0, le=50),  # noqa: WPS432
    yandex_music_client: YMClient = Depends(get_ymclient),
) -> List[models.NewRelease]:
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
    new_releases = await yandex_music_client.get_editorial_new_releases()
    return new_releases[offset : offset + limit]
