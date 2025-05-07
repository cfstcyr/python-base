import logging.config

import yaml

from .logs_settings import LogsSettings


def init_logs(logs_settings: LogsSettings):
    with open(logs_settings.log_config_path, "r") as file:
        log_config = yaml.safe_load(file)

    logging.config.dictConfig(log_config)
