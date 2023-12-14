from typing import List

from fastapi import APIRouter, Depends
from yandex_music import ClientAsync, DownloadInfo

from fefu_music.services.yandex_music_api import get_yandex_music_client, utils
from fefu_music.web.api.tracks.schema import DownloadInfoDTO, TrackDTO

router = APIRouter()


@router.get(
    "/tracks/{track_id}",
    response_model=TrackDTO,
)
async def get_track(
    track_id: int,
    yandex_music_client: ClientAsync = Depends(get_yandex_music_client),
) -> TrackDTO:
    """
    Asynchronous function to get a track from Yandex Music.

    This function uses the Yandex Music API to fetch a track by its ID. It also fetches
    the download information for the track.

    :param track_id: The ID of the track to fetch.
    :param yandex_music_client: An instance of the Yandex Music client.
    :return: A TrackDTO object containing the track data and download information.
    """
    track = (await yandex_music_client.tracks(track_id))[0]
    download_info = await track.get_download_info_async(get_direct_links=True)
    return TrackDTO(
        id=track.id,
        title=track.title,
        artists=track.artists,
        duration_ms=track.duration_ms,
        duration_text=utils.format_duration(track.duration_ms),
        cover_url=track.get_cover_url("400x400"),
        download_info=download_info,
    )


@router.get(
    "/tracks/{track_id}/download/info",
    response_model=DownloadInfoDTO,
)
async def get_download_info(
    track_id: int,
    yandex_music_client: ClientAsync = Depends(get_yandex_music_client),
) -> List[DownloadInfo]:
    """
    Asynchronous function to get the download information for a track from Yandex Music.

    This function uses the Yandex Music API to fetch the download information for a
    track by its ID.

    :param track_id: The ID of the track to fetch the download information for.
    :param yandex_music_client: An instance of the Yandex Music client.
    :return: A list of DownloadInfo objects containing the download information
             for the track.
    """
    return await yandex_music_client.tracks_download_info(
        track_id=track_id,
        get_direct_links=True,
    )
