import json

from fastapi.testclient import TestClient


def test_get_zen_resp_status(client: TestClient):
    resp = client.get('/api/v1/zen')
    assert resp.status_code == 200


def test_get_zen_resp_content(client: TestClient):
    resp = client.get('/api/v1/zen')

    content = json.loads(resp.content)

    assert isinstance(content.get('message'), str)
