from fastapi import FastAPI, Query
from typing import List, Optional
from starlette.status import HTTP_201_CREATED, HTTP_200_OK
from src.Modals.Sensor import Sensor
from src.Modals.Metrics import Metrics
from src.Utils.Database import connectDatabase, disconnectDatabase
from src.Service.SensorService import postSensorService, getSensorService
from src.Service.MetricService import postMetricsService, getMetricsService

app = FastAPI()

@app.get('/sensor/{id}', status_code=HTTP_200_OK)
def getSensor(id: str):
    return {'sensor': getSensorService(id)}

@app.post('/sensor', status_code=HTTP_201_CREATED)
def postSensor(sensor: Sensor):
    postSensorService(sensor)


@app.post('/metrics', status_code=HTTP_201_CREATED)
def postMetrics(metrics: Metrics):
    postMetricsService(metrics)

@app.get('/metrics', status_code=HTTP_200_OK)
def getSensorMetrics(
    sensor_id: Optional[List[str]] = Query(default=None),
    exclude_temperature: bool = False, 
    exclude_humidity: bool = False,
    date_range: Optional[int] = Query(default=None, ge=1, le=30)):
    print(type(exclude_temperature), exclude_temperature)
    return {"metrics": getMetricsService(sensor_id, exclude_temperature, exclude_humidity, date_range)}



@app.on_event("startup")
def createDatabaseConnection():
    connectDatabase()

@app.on_event("shutdown")
def disconnectDatabaseConnection():
    disconnectDatabase()