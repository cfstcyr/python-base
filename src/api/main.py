import logging

from fastapi import FastAPI

from api.settings import get_settings
from lib_core.logs import init_logs

init_logs(get_settings().logs)
logger = logging.getLogger(__name__)

app = FastAPI()

logger.info("Starting FastAPI application")

@app.get("/")
def read_root():
    return {"Hello": "World"}
