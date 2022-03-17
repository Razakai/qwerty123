from src.Utils.Database import database
from src.Modals.Metrics import Metrics
from datetime import datetime, date
from typing import List, Optional

def postMetricsDao(metrics: Metrics) -> None:
    currentDate = datetime.utcnow()
    
    query = "INSERT into metrics (sensor_id, temperature, humidity, timestamp) VALUES (:sensor_id, :temperature, :humidity, :timestamp)"
    values = {"sensor_id": metrics.sensorId, "temperature": metrics.temperature, "humidity": metrics.humidity, "timestamp": int(f"{currentDate.year}{currentDate.month}{currentDate.day}")}
    database.execute(query, False, values)

def getMetricsDao(
    sensorList: Optional[List[int]], 
    excludeTemperature: bool,
    excludeHumidity: bool,
    dateFrom: Optional[date] = None) -> list:
    
    query = """
    SELECT 
    CASE WHEN :excludeTemperature = False THEN avg(temperature) END AS AverageTemperature,
    CASE WHEN :excludeHumidity = False THEN avg(humidity) END AS AverageHumidity.
    WHERE 
        (ISNULL(:sensorList, 0) != 0 AND id in (:sensorList))
    AND (
        (ISNULL(:dateFrom, 0) != 0 AND timestamp >= :dateFrom)
    )
    """
    values = {"excludeTemperature": excludeTemperature, "excludeHumidity": excludeHumidity, "sensorList": sensorList, "dateFrom": dateFrom}

    return database.fetch(query=query, isOne=False, values=values)