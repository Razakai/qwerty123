from src.Dao.MetricDao import postMetricsDao, getMetricsDao, getRecentMetricsDao
from typing import List, Optional
from src.Modals.Metrics import Metrics
from fastapi import HTTPException
from src.Service.SensorService import doSensorsExistByIds
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from datetime import datetime, timedelta
import re


def postMetricsService(metrics: Metrics) -> None:
    if len(doSensorsExistByIds([metrics.sensor_id])) == 0:
        return postMetricsDao(metrics)

    raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Sensor ID: {metrics.sensor_id} does not exist")


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
        # remove any duplicates
        sensorList = list(set(sensorList))
        badQuerySensor = doSensorsExistByIds(sensorList)
        if len(badQuerySensor) > 0:
            badIds = []
            for row in badQuerySensor:
                badIds.append(row["id"])
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                                detail=f"Given sensor Id's do not exist: {', '.join(badIds)}")

    if dateRange is not None:
        # using full date excluding miliseconds as too large for sqlite
        dateFrom = str(datetime.utcnow() - timedelta(days=dateRange)).split('.')[0]
        dateFrom = int(re.sub('[^0-9]', '', dateFrom))

        data = getMetricsDao(dateFrom=dateFrom, sensorList=sensorList, excludeTemperature=excludeTemperature,
                             excludeHumidity=excludeHumidity)

    else:
        data = getRecentMetricsDao(sensorList=sensorList, excludeTemperature=excludeTemperature,
                                   excludeHumidity=excludeHumidity)

    if len(data) > 0:
        return data

    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No metric data found")
