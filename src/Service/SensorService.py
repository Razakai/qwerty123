from src.Modals.Sensor import Sensor
from src.Dao.SensorDao import postSensorDao, getSensorDao
from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND

def postSensorService(sensor: Sensor) -> None:
    postSensorDao(sensor)


def getSensorService(sensorId: int) -> dict:
    res = getSensorDao(sensorId)
    if res is not None:
        return dict(res)
    
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Sensor not Found")