import logging
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI

from api.settings import Settings
from lib_core.logs import setup_logs


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = Settings.create()
    setup_logs(settings.logs, settings)
    logging.getLogger("uvicorn").handlers.clear()

    log = structlog.get_logger().bind(name=app.title, version=app.version)
    log.info("Starting FastAPI application")

    yield

    log.info("Shutting down FastAPI application")


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World"}
