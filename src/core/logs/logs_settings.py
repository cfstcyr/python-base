from pathlib import Path

from pydantic import AliasChoices, Field, FilePath
from pydantic_settings import BaseSettings


class LogsSettings(BaseSettings):
    log_config_path: FilePath = Field(
        default=Path("logging.yaml"),
        validation_alias=AliasChoices("log_config", "log_config_path"),
        description=(
            "Path to the logging configuration file. "
            "The file should follow the [logging configuration dictionary schema](https://docs.python.org/3/library/logging.config.html#logging-config-dictschema)"
        ),
    )
