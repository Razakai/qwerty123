from fastapi.testclient import TestClient
from main import app

def test_post_sensor():
    with TestClient(app) as client:
        res = client.post('/sensor', json={"id": "1", "country": "Ireland", "city": "Cork"})

        assert res.status_code == 201


def test_post_sensor_bad_request():
    with TestClient(app) as client:
        res = client.post('/sensor', json={"country": "Ireland", "city": "Cork"})

        assert res.status_code == 422
        assert res.json() == {"detail": 
        [{
            "loc": [
                "body",
                "id"
            ],
            "msg": "field required",
            "type": "value_error.missing"
        }]}
        
