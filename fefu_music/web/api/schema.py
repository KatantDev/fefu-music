from typing import List

from pydantic import BaseModel, ConfigDict, HttpUrl, model_validator
from yandex_music import Album, Track

from fefu_music.services.yandex_music_api import utils


class ArtistShortDTO(BaseModel):
    """DTO to represent short information about artist."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class TrackShortDTO(BaseModel):
    """DTO to represent short information about track."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    cover_url: HttpUrl
    duration_ms: int
    duration_text: str
    artists: List[ArtistShortDTO]

    @model_validator(mode="before")
    def validate_model(cls, track: Track) -> Track:
        """
        Validate the model.

        :param track: The track to validate.
        :return: The validated track.
        """
        track.duration_text = utils.format_duration(track.duration_ms)
        track.cover_url = track.get_cover_url("100x100")
        return track


class AlbumShortDTO(BaseModel):
    """DTO to represent short information about the album."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    cover_url: HttpUrl
    track_count: int
    artists: List[ArtistShortDTO]
    release_date: str

    @model_validator(mode="before")
    def validate_model(cls, album: Album) -> Album:
        """
        Validate the model.

        :param album: The album to validate.
        :return: The validated album.
        """
        album.cover_url = album.get_cover_url("400x400")
        return album
