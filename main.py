from fastapi import FastAPI
from starlette.status import HTTP_201_CREATED, HTTP_200_OK
from src.Modals.Sensor import Sensor
from src.Modals.Metrics import Metrics
from src.Utils.Database import connectDatabase, disconnectDatabase
from src.Service.SensorService import postSensorService, getSensorService
from src.Service.MetricService import postMetricsService

app = FastAPI()

@app.get('/sensor/{id}', status_code=HTTP_200_OK)
def getSensor(id: int):
    return {'sensor': getSensorService(id)}

@app.post('/sensor', status_code=HTTP_201_CREATED)
def postSensor(sensor: Sensor):
    postSensorService(sensor)


@app.post('/metrics', status_code=HTTP_201_CREATED)
def postMetrics(metrics: Metrics):
    postMetricsService(metrics)



@app.on_event("startup")
def createDatabaseConnection():
    connectDatabase()

@app.on_event("shutdown")
def disconnectDatabaseConnection():
    disconnectDatabase()