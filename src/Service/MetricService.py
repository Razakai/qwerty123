from src.Dao.MetricDao import postMetricsDao, getMetricsDao, getRecentMetricsDao
from typing import List, Optional
from src.Modals.Metrics import Metrics
from fastapi import HTTPException
from src.Service.SensorService import getSensorService
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from datetime import datetime, timedelta
import re

def postMetricsService(metrics: Metrics) -> None:
    if getSensorService(metrics.sensor_id):
        postMetricsDao(metrics)

def getMetricsService(
    sensorList: Optional[List[str]], 
    excludeTemperature: bool, 
    excludeHumidity: bool,
    dateRange: Optional[int]) -> list:

    dateFrom = None
    data = []

    if excludeHumidity and excludeTemperature:
        # can't exclude both temerature and humidity
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="cannot exclude both temperature and humidity")
    
    # check if sensor ID's passed in are present
    if sensorList is not None:
        for id in sensorList:
            getSensorService(id)

    
    if dateRange is not None:
        # using full date including miliseconds is toolarge for sqlite
        dateFrom = str(datetime.utcnow() - timedelta(days=dateRange)).split('.')[0]
        dateFrom = int(re.sub('[^0-9]', '', dateFrom))
        for row in getMetricsDao(dateFrom=dateFrom, sensorList=sensorList):
            row = dict(row)
            if excludeTemperature:
                row.pop('AverageTemperature', None)
            if excludeHumidity:
                row.pop('AverageHumidity', None)
            data.append(row)

    else:
        for row in getRecentMetricsDao(sensorList=sensorList):
            row = dict(row)
            if excludeTemperature:
                row.pop('temperature', None)
            if excludeHumidity:
                row.pop('humidity', None)
            data.append(row)
    
    if len(data) > 0:
        return data
    
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No metric data found")
