from typing import List

from pydantic import BaseModel, ConfigDict, HttpUrl

from fefu_music.web.api.schema import TrackShortDTO


class DownloadInfoDTO(BaseModel):
    """DTO to represent download information."""

    model_config = ConfigDict(from_attributes=True)

    codec: str
    bitrate_in_kbps: int
    download_info_url: HttpUrl
    direct_link: HttpUrl


class TrackDTO(TrackShortDTO):
    """DTO to represent detail information about track."""

    download_info: List[DownloadInfoDTO]
