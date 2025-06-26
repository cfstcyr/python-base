from enum import Enum

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings


class Environment(Enum):
    """
    Enum for different environments.
    """

    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"
    STAGING = "staging"


class EnvSettings(BaseSettings):
    env: Environment = Field(
        default=Environment.DEVELOPMENT,
        validation_alias=AliasChoices("e", "env", "environment"),
        description="The environment in which the application is running.",
    )

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

    def is_testing(self) -> bool:
        """
        Check if the current environment is testing.

        Returns:
            bool: True if the environment is testing, False otherwise.
        """
        return self.env == Environment.TESTING

    def is_staging(self) -> bool:
        """
        Check if the current environment is staging.

        Returns:
            bool: True if the environment is staging, False otherwise.
        """
        return self.env == Environment.STAGING
