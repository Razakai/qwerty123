from src.Utils.Database import database
from src.Modals.Sensor import Sensor

def postSensorDao(sensor: Sensor) -> None:
    query = "INSERT INTO sensor values(:id, :country, :city)"
    values = {"id": sensor.id, "country": sensor.country, "city": sensor.city}

    res = database.execute(query=query, values=values, isMany=False)
    print(res.lastrowid)

def getSensorDao(sensor_id: int) -> Sensor:
    query = "SELECT * from sensor where id = :id"
    values = {"id": sensor_id}
    
    return database.fetch(query, True, values)
