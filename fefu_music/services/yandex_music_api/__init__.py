"""Yandex Music API service."""
from fefu_music.services.yandex_music_api.dependencies import get_yandex_music_client
from fefu_music.services.yandex_music_api.lifetime import startup

__all__ = ["startup", "get_yandex_music_client"]
