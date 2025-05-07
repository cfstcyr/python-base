from enum import Enum

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
    )

    logs: LogsSettings = LogsSettings()

    env: Environment = Field(
        default=Environment.DEVELOPMENT,
        validation_alias=AliasChoices("environment", "env"),
        description="The environment in which the application is running.",
    )

    def is_dev(self) -> bool:
        """
        Check if the current environment is development.
        """
        return self.env == Environment.DEVELOPMENT

    def is_prod(self) -> bool:
        """
        Check if the current environment is production.
        """
        return self.env == Environment.PRODUCTION
