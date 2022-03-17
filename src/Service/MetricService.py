from src.Dao.MetricDao import postMetricsDao, getMetricsDao
from typing import List, Optional
from src.Modals.Metrics import Metrics
from fastapi import HTTPException
from src.Service.SensorService import getSensorService
from starlette.status import HTTP_400_BAD_REQUEST
from datetime import datetime, timedelta

def postMetricsService(metrics: Metrics) -> None:
    if getSensorService(metrics.sensorId):
        postMetricsDao(metrics)

def getMetricsService(
    sensorList: Optional[List[int]], 
    excludeTemperature: bool, 
    excludeHumidity: bool,
    dateRange: Optional[int]) -> list:

    dateFrom = None

    if excludeHumidity and excludeTemperature:
        # can't exclude both temerature and humidity
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="cannot exclude both temperature and humidity")
    
    # check if sensor ID's passed in are present
    if sensorList is not None:
        for id in sensorList:
            getSensorService(id)
    
    if dateRange is not None:
        dateFrom = datetime.utcnow() - timedelta(days=dateRange)
    
    return getMetricsDao(sensorList, excludeTemperature, excludeHumidity, dateFrom)