from functools import lru_cache

from lib_core.settings import AppBaseSettings


class Settings(AppBaseSettings):
    pass


@lru_cache()
def get_settings() -> Settings:
    """
    Get the application settings.
    """
    return Settings()  # type: ignore
