from fastapi.testclient import TestClient
from main import app


def test_post_metric():
    with TestClient(app) as client:
        # first post sensor
        client.post('/sensor', json={"id": "1", "country": "Ireland", "city": "Cork"})

        res = client.post('/metrics', json={"sensor_id": "1", "temperature": 25.99, "humidity": 45.3})

        assert res.status_code == 201


def test_posty_metric_invalid_type():
    with TestClient(app) as client:
        # first post sensor
        client.post('/sensor', json={"id": "1", "country": "Ireland", "city": "Cork"})

        res = client.post('/metrics', json={"sensor_id": "1", "temperature": 25.99, "humidity": "bees"})

        assert res.status_code == 422
        assert res.json() == {
            "detail": 
                [
                    {
                    "loc": [
                        "body",
                        "humidity"
                    ],
                    "msg": "value is not a valid float",
                    "type": "type_error.float"
                    }
                ]
            }


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


def test_get_recent_metric_filter_by_id_and_exclude_humidity():
    with TestClient(app) as client:
        # first post sensors
        client.post('/sensor', json={"id": "1", "country": "Ireland", "city": "Cork"})
        client.post('/sensor', json={"id": "2", "country": "Ireland", "city": "Galway"})

        client.post('/metrics', json={"sensor_id": "1", "temperature": 25.99, "humidity": 45.3})

        client.post('/metrics', json={"sensor_id": "2", "temperature": 12, "humidity": 15})
       
        res = client.get('/metrics?sensor_id=1&exclude_humidity=True')

        assert res.status_code == 200
        assert res.json() == {"metrics": 
        [
            {
                "temperature": 25.99,
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


def test_get_metrics_filter_by_id_thats_not_present():
    with TestClient(app) as client:
        res = client.get('/metrics?sensor_id=1')

        assert res.status_code == 400
        assert res.json() == {"detail": "Given sensor Id's do not exist: 1"}


def test_get_metrics_with_none_posted():
     with TestClient(app) as client:
        # first post sensors
        client.post('/sensor', json={"id": "1", "country": "Ireland", "city": "Cork"})
        client.post('/sensor', json={"id": "2", "country": "Ireland", "city": "Galway"})

        res = client.get('/metrics')

        assert res.status_code == 404
        assert res.json() == {"detail": "No metric data found"}


def test_get_average_metrics():
    with TestClient(app) as client:
        # first post sensors
        client.post('/sensor', json={"id": "1", "country": "Ireland", "city": "Cork"})
        client.post('/sensor', json={"id": "2", "country": "Ireland", "city": "Galway"})

        client.post('/metrics', json={"sensor_id": "1", "temperature": 25.99, "humidity": 45.3})
        client.post('/metrics', json={"sensor_id": "1", "temperature": 30, "humidity": 99})
        client.post('/metrics', json={"sensor_id": "1", "temperature": 12, "humidity": 8})

        client.post('/metrics', json={"sensor_id": "2", "temperature": 12, "humidity": 15})

        res = client.get('/metrics?date_range=15')

        assert res.status_code == 200
        assert res.json() == {
        "metrics": 
            [
                {
                "AverageTemperature": 22.66333333333333,
                "AverageHumidity": 50.76666666666667,
                "sensor_id": "1"
                },
                {
                "AverageTemperature": 12.0,
                "AverageHumidity": 15.0,
                "sensor_id": "2"
                }
            ]
        }