from src.Modals.Sensor import Sensor
from src.Dao.SensorDao import postSensorDao, getSensorDao
from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

def doesSensorExistById(sensor_id: str) -> dict:
    res = getSensorDao(sensor_id)
    print(res) 
    return True if res is not None else False

def postSensorService(sensor: Sensor) -> None:
    if not doesSensorExistById(sensor.id):
        return postSensorDao(sensor)
    
    raise HTTPException(status_code=HTTP_409_CONFLICT, detail="Sensor ID Already Exists")

def getSensorService(sensor_id: str) -> dict:
    res = getSensorDao(sensor_id)
    if res is not None:
        return dict(res)
    
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"Sensor ID {sensor_id} not Found")