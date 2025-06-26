import structlog
from pydantic_settings import CliApp

from lib_core.foo import bar
from lib_core.logs import setup_logs
from lib_core.settings.app_base_settings import AppBaseSettings


class Settings(AppBaseSettings):
    def cli_cmd(self) -> None:
        setup_logs(self.logs, self)

        log = structlog.get_logger()
        log.info("Starting application...")

        bar()


def main() -> None:
    CliApp.run(Settings)
