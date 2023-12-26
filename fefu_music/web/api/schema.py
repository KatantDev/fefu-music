from datetime import datetime
from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict, HttpUrl, computed_field, model_validator
from ymdantic.models import Album, Artist, TrackType
from ymdantic.models.landing.landing_artist import LandingArtist

from fefu_music.services.yandex_music_api import utils

ArtistType = Union[LandingArtist, Artist]


class ArtistShortDTO(BaseModel):
    """DTO to represent short information about artist."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    cover_url: HttpUrl

    @model_validator(mode="before")
    def cover_url_validator(cls, obj: Artist) -> Artist:
        """
        Inject cover url to object.

        :param obj: The artist to inject.
        :return: The artist with injected field.
        """
        return obj.model_copy(
            update={"cover_url": obj.get_cover_image_url("100x100")},
        )


class TrackShortDTO(BaseModel):
    """DTO to represent short information about track."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    cover_url: Optional[HttpUrl] = None
    duration_ms: int
    artists: List[ArtistShortDTO]

    @model_validator(mode="before")
    def cover_url_validator(cls, obj: TrackType) -> TrackType:
        """
        Inject cover url to object.

        :param obj: The track to inject.
        :return: The track with injected field.
        """
        return obj.model_copy(
            update={"cover_url": obj.get_cover_image_url("100x100")},
        )

    @computed_field  # type: ignore[misc]
    @property
    def duration_text(self) -> str:
        """
        Get duration text by formatting duration in milliseconds.

        :return: The duration text.
        """
        return utils.format_duration(self.duration_ms)


class AlbumShortDTO(BaseModel):
    """DTO to represent short information about the album."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    cover_url: HttpUrl
    track_count: int
    artists: List[ArtistShortDTO]
    release_date: datetime

    @model_validator(mode="before")
    def cover_url_validator(cls, obj: Album) -> Album:
        """
        Inject cover url to object.

        :param obj: The album to inject.
        :return: The album with injected field.
        """
        return obj.model_copy(
            update={"cover_url": obj.get_cover_image_url("400x400")},
        )
