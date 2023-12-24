from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, HttpUrl, model_validator
from ymdantic.models import NewRelease
from ymdantic.models.landing.landing_album import LandingAlbum
from ymdantic.models.landing.landing_artist import LandingArtist


class LandingAlbumDTO(BaseModel):
    """DTO to represent short information about the album."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    cover_url: HttpUrl
    album_type: Optional[Literal["single"]] = None

    @model_validator(mode="before")
    def cover_url_validator(cls, obj: LandingAlbum) -> LandingAlbum:
        """
        Inject cover url to object.

        :param obj: The album to inject.
        :return: The album with injected field.
        """
        return obj.model_copy(
            update={"cover_url": obj.get_cover_image_url("400x400")},
        )


class LandingArtistDTO(BaseModel):
    """DTO to represent short information about the album."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    cover_url: HttpUrl

    @model_validator(mode="before")
    def cover_url_validator(cls, obj: LandingArtist) -> LandingArtist:
        """
        Inject cover url to object.

        :param obj: The artist to inject.
        :return: The artist with injected field.
        """
        return obj.model_copy(
            update={"cover_url": obj.get_cover_image_url("100x100")},
        )


class NewReleaseDTO(BaseModel):
    """DTO to represent short information about the album."""

    model_config = ConfigDict(from_attributes=True)

    cover_url: HttpUrl
    artists: List[LandingArtistDTO]
    album: LandingAlbumDTO
    release_date: datetime

    @model_validator(mode="before")
    def cover_url_validator(cls, obj: NewRelease) -> NewRelease:
        """
        Inject cover url to object.

        :param obj: The new release to inject.
        :return: The new release with injected field.
        """
        return obj.model_copy(
            update={"cover_url": obj.get_cover_image_url("400x400")},
        )
