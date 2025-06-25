import logging

from pydantic_settings import CliApp

from lib_core.foo import bar
from lib_core.logs import init_logs
from lib_core.settings.app_base_settings import AppBaseSettings

logger = logging.getLogger(__name__)


class Settings(AppBaseSettings):
    def cli_cmd(self) -> None:
        init_logs(self.logs)

        logger.info("Starting application...")

        bar()


def main() -> None:
    CliApp.run(Settings)
