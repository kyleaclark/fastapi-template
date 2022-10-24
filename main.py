import logging

from app.config.app_init import create_app
from app.config.app_config import AppConfig


logger = logging.getLogger(__name__)

# instantiate app configuration as early as possible to initialize loggers
cfg = AppConfig()

# create FastAPI app instance
app = create_app()


def run_app_locally():
    import uvicorn

    logger.info(f'')

    uvicorn.run(app, host='localhost', port=8000)

    logger.info('App running')


if __name__ == '__main__':
    run_app_locally()
