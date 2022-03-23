from src.Modals.Sensor import Sensor
from src.Dao.SensorDao import postSensorDao, getSensorDao, doSensorsExistByIdsDao
from typing import List
from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT


def doSensorsExistByIds(sensor_id: List[str]) -> list:
    return doSensorsExistByIdsDao(sensor_id)


def postSensorService(sensor: Sensor) -> None:
    if len(doSensorsExistByIds([sensor.id])) == 1:
        return postSensorDao(sensor)

    raise HTTPException(status_code=HTTP_409_CONFLICT, detail="Sensor ID Already Exists")


def getSensorService(sensor_id: str) -> dict:
    res = getSensorDao(sensor_id)
    if res is not None:
        return dict(res)

    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"Sensor ID {sensor_id} not Found")
