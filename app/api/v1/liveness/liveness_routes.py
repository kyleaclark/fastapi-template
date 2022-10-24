import datetime as dt

from fastapi import APIRouter

from app.api.v1.liveness.liveness_models import LivenessGetResModel
from app.config.app_config import cfg


router = APIRouter()


@router.get('/liveness', response_model=LivenessGetResModel)
async def get_liveness() -> LivenessGetResModel:
    result = LivenessGetResModel(
        appStartDatetimeUTC=cfg.settings.app_start_datetime_utc,
        environment=cfg.settings.env,
        deployedFlag=cfg.settings.deployed_flag,
        requestDatetimeUTC=dt.datetime.utcnow().isoformat()
    )

    return result
