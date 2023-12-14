from typing import List

from pydantic import BaseModel, ConfigDict, HttpUrl


class ArtistShortDTO(BaseModel):
    """DTO to represent short information about artist."""

    model_config = ConfigDict(from_attributes=True)

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
