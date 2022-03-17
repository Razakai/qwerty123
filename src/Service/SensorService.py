from src.Modals.Sensor import Sensor
from src.Dao.SensorDao import postSensorDao, getSensorDao
from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

def doesSensorExistById(sensorId: int) -> dict:
    res = getSensorDao(sensorId)
    return True if res is not None else False

def postSensorService(sensor: Sensor) -> None:
    if doesSensorExistById(sensor.id):
        postSensorDao(sensor)
    
    raise HTTPException(status_code=HTTP_409_CONFLICT, detail="Sensor ID Already Exists")

def getSensorService(sensorId: int) -> dict:
    res = getSensorDao(sensorId)
    if res is not None:
        return dict(res)
    
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Sensor not Found")