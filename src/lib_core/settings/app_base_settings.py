from enum import Enum
from functools import lru_cache
from typing import Self

from pydantic_settings import SettingsConfigDict

from lib_core.logs.logs_settings import LogsSettings

from .env_settings import EnvSettings


class Environment(Enum):
    """
    Enum for different environments.
    """

    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"
    STAGING = "staging"


class AppBaseSettings(EnvSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )

    logs: LogsSettings = LogsSettings()

    @classmethod
    @lru_cache
    def create(cls) -> Self:
        """
        Create the settings instance.

        Returns:
            Self: An instance of the application settings.
        """
        return cls()
