from src.Utils.Database import execute, fetch
from src.Modals.Sensor import Sensor
from typing import List

def postSensorDao(sensor: Sensor) -> None:
    query = "INSERT INTO sensor values(:id, :country, :city)"
    values = {"id": sensor.id, "country": sensor.country, "city": sensor.city}

    execute(query=query, values=values, isMany=False)

def getSensorDao(sensor_id: str) -> Sensor:
    query = "SELECT * from sensor where id = :id"
    values = {"id": sensor_id}
    
    return fetch(query, True, values)

def doSensorsExistByIdsDao(sensorList: List[str]) -> list:
    # first delete temp table if it already exists
    deleteTempQuery = "DROP TABLE IF EXISTS temp.sensorList"
    # create new temp table with the new sensorList values
    createTempTable = "CREATE TEMPORARY TABLE sensorList (id varchar2(255))"
    insertIntoTemp = "INSERT INTO temp.sensorList values (?)"
    # Get all query ID's that have no corresponding sensor id
    getInvalidIds = f"""
    SELECT tmp.id
    FROM temp.sensorList tmp
    LEFT JOIN sensor sen ON tmp.id = sen.id
    WHERE sen.id is null
    """

    execute(isMany=False, query=deleteTempQuery)
    execute(isMany=False, query=createTempTable)
    if len(sensorList) > 1:
        execute(isMany=True, query=insertIntoTemp, values=[[x] for x in sensorList])
    else:
        execute(isMany=False, query=insertIntoTemp, values=sensorList)
    return fetch(isOne=False, query=getInvalidIds)

    