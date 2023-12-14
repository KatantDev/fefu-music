from typing import List

from pydantic import ConfigDict, model_validator
from yandex_music import Album

from fefu_music.web.api.schema import AlbumShortDTO, TrackShortDTO


class AlbumDTO(AlbumShortDTO):
    """DTO to represent detail information about the album."""

    model_config = ConfigDict(from_attributes=True)

    tracks: List[TrackShortDTO]

    @model_validator(mode="before")
    def validate_tracks(cls, album: Album) -> Album:
        """
        Validate the tracks.

        :param album: The album to validate.
        :return: The validated album.
        """
        album.tracks = [track for volume in album.volumes for track in volume]
        return album
