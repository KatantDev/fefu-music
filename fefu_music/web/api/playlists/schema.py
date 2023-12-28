from datetime import datetime
from typing import List, Optional

from pydantic import ConfigDict, computed_field, model_validator
from ymdantic.models import Playlist

from fefu_music.services.yandex_music_api import utils
from fefu_music.web.api.schema import PlaylistShortDTO, TrackShortDTO


class PlaylistDTO(PlaylistShortDTO):
    """DTO to represent detail information about the album."""

    model_config = ConfigDict(from_attributes=True)

    description: str
    track_count: int
    duration_ms: int
    modified: datetime
    likes_count: Optional[int] = None
    tracks: List[TrackShortDTO]
    similar_playlists: List[PlaylistShortDTO]

    @computed_field  # type: ignore[misc]
    @property
    def duration_text(self) -> str:
        """
        Get duration text by formatting duration in milliseconds.

        :return: The duration text.
        """
        return utils.format_duration(self.duration_ms)

    @model_validator(mode="before")
    def tracks_validator(cls, obj: Playlist) -> Playlist:
        """
        Validate the tracks.

        :param obj: The album to validate.
        :return: The validated album.
        """
        return obj.model_copy(
            update={"tracks": [playlist_track.track for playlist_track in obj.tracks]},
        )
