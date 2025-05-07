import logging

from app.settings import get_settings
from core.foo import bar
from core.logs import init_logs

logger = logging.getLogger(__name__)


def main(*, settings=get_settings()):
    init_logs(settings.logs)

    logger.info("Starting application...")

    print(bar())
