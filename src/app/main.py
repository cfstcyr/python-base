import logging

from config.logs import init_logs
from core.foo import bar

logger = logging.getLogger(__name__)

def main():
    init_logs()

    logger.info("Starting application...")

    print(bar())
