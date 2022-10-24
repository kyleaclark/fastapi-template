import logging

from fastapi.applications import FastAPI

from app.api.api_router import api_router
from app.config.app_config import cfg


logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    logger.info('Begin creating fastapi app new instance')

    result = FastAPI(root_path=cfg.settings.root_dir)
    result.include_router(api_router, prefix='')

    return result
