from typing import List

from pydantic import BaseModel, HttpUrl

from fefu_music.web.api.schema import ArtistShortDTO


class AlbumDTO(BaseModel):
    """DTO to represent short information about the album."""

    id: int
    title: str
    cover_url: HttpUrl
    track_count: int
    artists: List[ArtistShortDTO]
    release_date: str
