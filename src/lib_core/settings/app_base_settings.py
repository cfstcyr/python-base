from enum import Enum
from functools import lru_cache
from typing import Self

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from lib_core.logs.logs_settings import LogsSettings


class Environment(Enum):
    """
    Enum for different environments.
    """

    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"
    STAGING = "staging"


class AppBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )

    logs: LogsSettings = LogsSettings()

    env: Environment = Field(
        default=Environment.DEVELOPMENT,
        validation_alias=AliasChoices("e", "env", "environment"),
        description="The environment in which the application is running.",
    )

    @classmethod
    @lru_cache
    def create(cls) -> Self:
        """
        Create the settings instance.

        Returns:
            Self: An instance of the application settings.
        """
        return cls()

    def is_dev(self) -> bool:
        """
        Check if the current environment is development.

        Returns:
            bool: True if the environment is development, False otherwise.
        """
        return self.env == Environment.DEVELOPMENT

    def is_prod(self) -> bool:
        """
        Check if the current environment is production.

        Returns:
            bool: True if the environment is production, False otherwise.
        """
        return self.env == Environment.PRODUCTION
