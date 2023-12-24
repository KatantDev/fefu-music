from typing import List, Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from ymdantic import YMClient, models

from fefu_music.services.yandex_music_api import get_ymclient
from fefu_music.web.api.tracks.schema import DownloadInfoDTO, TrackDTO

router = APIRouter()


@router.get(
    "/tracks/{track_id}",
    response_model=TrackDTO,
)
async def get_track(
    track_id: int,
    yandex_music_client: YMClient = Depends(get_ymclient),
) -> TrackDTO:
    """
    Asynchronous function to get a track from Yandex Music.

    This function uses the Yandex Music API to fetch a track by its ID. It also fetches
    the download information for the track.

    :param track_id: The ID of the track to fetch.
    :param yandex_music_client: An instance of the Yandex Music client.
    :raises HTTPException: If the track is not available.
    :return: A TrackDTO object containing the track data and download information.
    """
    track = await yandex_music_client.get_track(track_id)
    if track.available is False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Track is not available",
        )
    return TrackDTO.model_validate(
        track,
        context={
            "download_info": await track.get_download_info_direct(),
        },
    )


@router.get(
    "/tracks/{track_id}/download-info",
    response_model=List[DownloadInfoDTO],
)
async def get_download_info(
    track_id: int,
    yandex_music_client: YMClient = Depends(get_ymclient),
) -> Sequence[models.DownloadInfoDirect]:
    """
    Asynchronous function to get the download information for a track from Yandex Music.

    This function uses the Yandex Music API to fetch the download information for a
    track by its ID.

    :param track_id: The ID of the track to fetch the download information for.
    :param yandex_music_client: An instance of the Yandex Music client.
    :return: A list of DownloadInfo objects containing the download information
             for the track.
    """
    return await yandex_music_client.get_track_download_info_direct(track_id=track_id)
