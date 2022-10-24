import datetime as dt

import requests
from fastapi import APIRouter

from app.api.v1.zen.zen_models import ZenGetResModel


router = APIRouter()


@router.get('/zen', response_model=ZenGetResModel)
async def get_zen() -> ZenGetResModel:
    try:
        resp = requests.get('https://api.github.com/zen')
        message = f'Zen message: {resp.text}'
    except requests.exceptions.HTTPError:
        message = 'Zen message not found (HTTP Error)'
    except requests.RequestException:
        message = 'Zen message not found (Request Error)'
    except Exception:
        message = 'Zen message not found (Unknown Error)'

    result = ZenGetResModel(message=message)

    return result
