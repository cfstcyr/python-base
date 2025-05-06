from enum import Enum
from pathlib import Path

from pydantic import AliasChoices, Field, FilePath
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(Enum):
    """
    Enum for different environments.
    """
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"
    STAGING = "staging"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )

    log_config_path: FilePath = Field(
        default=Path("logging.yaml"),
        validation_alias=AliasChoices("log_config", "log_config_path"),
        description=(
            "Path to the logging configuration file. "
            "The file should follow the [logging configuration dictionary schema](https://docs.python.org/3/library/logging.config.html#logging-config-dictschema)"
        ),
    )

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
