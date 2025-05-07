from pathlib import Path

import pytest

from app.settings import Settings
from lib_core.logs.logs_settings import LogsSettings
from lib_core.settings.app_base_settings import Environment


@pytest.fixture
def settings():
    return Settings(
        env=Environment.TESTING,
        logs=LogsSettings(
            logs_config_path=Path("logging.test.yaml"),
        ),
    )
