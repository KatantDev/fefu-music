import enum
from datetime import timedelta
from pathlib import Path
from tempfile import gettempdir
from typing import List, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL

TEMP_DIR = Path(gettempdir())


class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    host: str = "127.0.0.1"
    port: int = 8000
    # quantity of workers for uvicorn
    workers_count: int = 1
    # Enable uvicorn reloading
    reload: bool = False

    # Current environment
    environment: str = "dev"

    log_level: LogLevel = LogLevel.INFO

    # Variables for the database
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "fefu_music"
    db_pass: str = "fefu_music"
    db_base: str = "fefu_music"
    db_echo: bool = False

    # Yandex Music API settings
    yandex_music_token: Optional[str] = None

    # Variables for the JWT
    secret_key: str = "secret"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 30

    # GitHub OAuth settings
    github_client_id: Optional[str] = None
    github_client_secret: Optional[str] = None

    # CORS settings
    cors_allow_origins: List[str] = ["*"]

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="postgres",
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_pass,
            path=f"/{self.db_base}",
        )

    @property
    def access_token_expire_timedelta(self) -> timedelta:
        """
        Get access token expiration timedelta.

        :return: timedelta.
        """
        return timedelta(minutes=self.access_token_expire_minutes)

    @property
    def refresh_token_expire_timedelta(self) -> timedelta:
        """
        Get refresh token expiration timedelta.

        :return: timedelta.
        """
        return timedelta(days=self.refresh_token_expire_days)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="FEFU_MUSIC_",
        env_file_encoding="utf-8",
    )


settings = Settings()
