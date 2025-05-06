import logging.config

import yaml

from ..settings import get_settings


def init_logs():
    with open(get_settings().log_config_path, "r") as file:
        log_config = yaml.safe_load(file)

    logging.config.dictConfig(log_config)
