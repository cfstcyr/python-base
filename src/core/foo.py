import logging

logger = logging.getLogger(__name__)


def bar():
    logger.debug("%s called", bar.__name__)
    return "bar"
