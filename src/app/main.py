import logging

from core.foo import bar
from core.logs import init_logs

logger = logging.getLogger(__name__)

def main():
    init_logs()

    logger.info("Starting application...")

    print(bar())
