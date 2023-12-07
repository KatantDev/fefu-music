from typing import List

from pydantic import BaseModel, HttpUrl


class ArtistShortDTO(BaseModel):
    """DTO to represent short information about artist."""

    id: int
    name: str


class TrackShortDTO(BaseModel):
    """DTO to represent short information about track."""

    id: int
    title: str
    cover_url: HttpUrl
    duration_ms: int
    duration_text: str
    artists: List[ArtistShortDTO]


class AlbumDTO(BaseModel):
    """DTO to represent short information about the album."""

    id: int
    title: str
    cover_url: HttpUrl
    track_count: int
