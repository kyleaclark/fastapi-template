import datetime as dt
import json

from fastapi.testclient import TestClient

from app.config.app_config import cfg


def test_get_readiness_resp_status(client: TestClient):
    resp = client.get('/api/v1/readiness')
    assert resp.status_code == 200


def test_get_readiness_resp_content(client: TestClient):
    before_req_datetime = dt.datetime.utcnow()
    resp = client.get('/api/v1/readiness')
    after_req_datetime = dt.datetime.utcnow()

    content = json.loads(resp.content)

    assert content.get('environment') == cfg.settings.env
    assert content.get('deployedFlag') == cfg.settings.deployed_flag
    assert (
            dt.datetime.strptime(content.get('appStartDatetimeUTC'), '%Y-%m-%dT%H:%M:%S.%f') ==
            dt.datetime.strptime(cfg.settings.app_start_datetime_utc, '%Y-%m-%dT%H:%M:%S.%f')
    )
    assert dt.datetime.strptime(content.get('requestDatetimeUTC'), '%Y-%m-%dT%H:%M:%S.%f') > before_req_datetime
    assert dt.datetime.strptime(content.get('requestDatetimeUTC'), '%Y-%m-%dT%H:%M:%S.%f') < after_req_datetime
