from typing import List

from pydantic import ConfigDict, model_validator
from ymdantic.models import Album

from fefu_music.web.api.schema import AlbumShortDTO, TrackShortDTO


class AlbumDTO(AlbumShortDTO):
    """DTO to represent detail information about the album."""

    model_config = ConfigDict(from_attributes=True)

    tracks: List[TrackShortDTO]

    @model_validator(mode="before")
    def tracks_validator(cls, obj: Album) -> Album:
        """
        Validate the tracks.

        :param obj: The album to validate.
        :return: The validated album.
        """
        return obj.model_copy(
            update={"tracks": [track for volume in obj.volumes for track in volume]},
        )
