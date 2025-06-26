import logging

from pydantic_settings import BaseSettings


class LogsSettings(BaseSettings):
    log_level: int | str = logging.INFO
    dev_log_level: int | str = logging.DEBUG

    is_gcp: bool = True

    logger_names: list[str] = [
        "root",
        "uvicorn",
        "uvicorn.error",
        "uvicorn.access",
        "gunicorn",
        "fastapi",
        "sqlalchemy.engine",
        "sqlalchemy.orm",
        "sqlalchemy.poolstarlette",
        "asyncio",
        "httpx",
        "botocore",
        "boto3",
        "google",
    ]
    logger_names_extends: list[str] = []
