import datetime as dt

from fastapi import APIRouter

from app.api.v1.readiness.readiness_models import ReadinessGetResModel
from app.config.app_config import cfg


router = APIRouter()


@router.get('/readiness', response_model=ReadinessGetResModel)
async def get_readiness() -> ReadinessGetResModel:
    result = ReadinessGetResModel(
        appStartDatetimeUTC=cfg.settings.app_start_datetime_utc,
        environment=cfg.settings.env,
        deployedFlag=cfg.settings.deployed_flag,
        requestDatetimeUTC=dt.datetime.utcnow().isoformat()
    )

    return result
