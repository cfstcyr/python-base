import logging

from app.settings import Settings, get_settings
from lib_core.foo import bar
from lib_core.logs import init_logs

logger = logging.getLogger(__name__)


def main(*, settings: Settings = get_settings()):
    init_logs(settings.logs)

    logger.info("Starting application...")

    bar()
