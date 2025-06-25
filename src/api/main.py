import logging

from fastapi import FastAPI

from api.settings import Settings
from lib_core.logs import init_logs

settings = Settings.create()
init_logs(settings.logs)
logger = logging.getLogger(__name__)

app = FastAPI()

logger.info("Starting FastAPI application")


@app.get("/")
def read_root():
    return {"Hello": "World"}
