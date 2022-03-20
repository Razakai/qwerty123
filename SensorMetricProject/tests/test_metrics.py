from fastapi.testclient import TestClient
from main import app


def test_post_metric():
    with TestClient(app) as client:
        # first post sensor
        client.post('/sensor', json={"id": "1", "country": "Ireland", "city": "Cork"})

        res = client.post('/metrics', json={"sensor_id": "1", "temperature": 25.99, "humidity": 45.3})

        assert res.status_code == 201


def test_get_recent_metric():
    with TestClient(app) as client:
        # first post sensors
        client.post('/sensor', json={"id": "1", "country": "Ireland", "city": "Cork"})
        client.post('/sensor', json={"id": "2", "country": "Ireland", "city": "Galway"})

        client.post('/metrics', json={"sensor_id": "1", "temperature": 25.99, "humidity": 45.3})
        client.post('/metrics', json={"sensor_id": "2", "temperature": 12, "humidity": 15})

        res = client.get('/metrics')

        assert res.status_code == 200
        assert res.json() == {"metrics": 
        [
            {
                "temperature": 25.99,
                "humidity": 45.3,
                "sensor_id": "1"
            },
            {
                "temperature": 12,
                "humidity": 15,
                "sensor_id": "2"
            }
        ]}

def test_get_recent_metric_filter_by_id():
    with TestClient(app) as client:
        # first post sensors
        client.post('/sensor', json={"id": "1", "country": "Ireland", "city": "Cork"})
        client.post('/sensor', json={"id": "2", "country": "Ireland", "city": "Galway"})

        client.post('/metrics', json={"sensor_id": "1", "temperature": 25.99, "humidity": 45.3})
        client.post('/metrics', json={"sensor_id": "2", "temperature": 12, "humidity": 15})

        res = client.get('/metrics?sensor_id=1')

        assert res.status_code == 200
        assert res.json() == {"metrics": 
        [
            {
                "temperature": 25.99,
                "humidity": 45.3,
                "sensor_id": "1"
            }
        ]}

def test_get_recent_metric_filter_by_id_and_exclude_temperature():
    with TestClient(app) as client:
        # first post sensors
        client.post('/sensor', json={"id": "1", "country": "Ireland", "city": "Cork"})
        client.post('/sensor', json={"id": "2", "country": "Ireland", "city": "Galway"})

        client.post('/metrics', json={"sensor_id": "1", "temperature": 25.99, "humidity": 45.3})
        client.post('/metrics', json={"sensor_id": "2", "temperature": 12, "humidity": 15})

        res = client.get('/metrics?sensor_id=1&exclude_temperature=True')

        assert res.status_code == 200
        assert res.json() == {"metrics": 
        [
            {
                "humidity": 45.3,
                "sensor_id": "1"
            }
        ]}

def test_get_recent_metric_filter_by_id_and_exclude_temperature_and_humidity():
    with TestClient(app) as client:
        # first post sensors
        client.post('/sensor', json={"id": "1", "country": "Ireland", "city": "Cork"})
        client.post('/sensor', json={"id": "2", "country": "Ireland", "city": "Galway"})

        client.post('/metrics', json={"sensor_id": "1", "temperature": 25.99, "humidity": 45.3})
        client.post('/metrics', json={"sensor_id": "2", "temperature": 12, "humidity": 15})

        res = client.get('/metrics?sensor_id=1&exclude_temperature=True&exclude_humidity=True')

        assert res.status_code == 400
        assert res.json() == {"detail": "cannot exclude both temperature and humidity"}