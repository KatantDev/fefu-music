from typing import List

from pydantic import BaseModel, ConfigDict, HttpUrl, ValidationInfo, model_validator
from ymdantic.models import TrackType

from fefu_music.web.api.schema import TrackShortDTO


class DownloadInfoDTO(BaseModel):
    """DTO to represent download information."""

    model_config = ConfigDict(from_attributes=True)

    codec: str
    bitrate_in_kbps: int
    direct_url: HttpUrl


class TrackDTO(TrackShortDTO):
    """DTO to represent detail information about track."""

    model_config = ConfigDict(from_attributes=True)

    download_info: List[DownloadInfoDTO]

    @model_validator(mode="before")
    def download_info_validator(cls, obj: TrackType, info: ValidationInfo) -> TrackType:
        """
        Inject download information to object.

        :param obj: The track to inject.
        :param info: The validation info.
        :return: The track with injected field.
        """
        if info.context is None:
            return obj
        return obj.model_copy(
            update={"download_info": info.context.get("download_info")},
        )
