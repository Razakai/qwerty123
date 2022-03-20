from src.Utils.Database import database
from src.Modals.Metrics import Metrics
from datetime import datetime
from typing import List, Optional
import re

def postMetricsDao(metrics: Metrics) -> None:
    # using full date including miliseconds is toolarge for sqlite
    currentDate = str(datetime.utcnow()).split('.')[0]
    timestamp = int(re.sub('[^0-9]', '', currentDate))
    
    query = "INSERT into metrics (sensor_id, temperature, humidity, timestamp) VALUES (:sensor_id, :temperature, :humidity, :timestamp)"
    values = {"sensor_id": metrics.sensor_id, "temperature": metrics.temperature, "humidity": metrics.humidity, "timestamp": timestamp}
    database.execute(query, False, values)


def getRecentMetricsDao(
    sensorList: Optional[List[str]] = None) -> list:

    query = f"""
    SELECT 
    met1.temperature,
    met1.humidity,
    met1.sensor_id
    FROM metrics met1
    WHERE met1.id = (SELECT met2.id
                    FROM metrics met2
                    WHERE met2.sensor_id = met1.sensor_id    
                    ORDER BY met2.timestamp DESC
                    LIMIT 1)
    AND
    CASE 
        WHEN ? > 0 THEN sensor_id in ({','.join('?' * (len(sensorList) if sensorList is not None else 0))})
        ELSE sensor_id = sensor_id 
    END
    """
    values = [len(sensorList) if sensorList is not None else 0]
    if sensorList is not None:
        values.extend(sensorList)
   
    return database.fetch(query=query, isOne=False, values=values)

def getMetricsDao(
    dateFrom: int,
    sensorList: Optional[List[str]] = []) -> list:
    
    query = f"""
    SELECT 
    avg(temperature) AS AverageTemperature,
    avg(humidity) AS AverageHumidity,
    sensor_id
    FROM metrics
    WHERE 
        timestamp >= ?
        AND
        CASE 
            WHEN ? > 0 THEN sensor_id in ({','.join('?' * (len(sensorList) if sensorList is not None else 0))})
        ELSE
            sensor_id = sensor_id 
        END
    GROUP BY sensor_id
    """

    values = [dateFrom, len(sensorList) if sensorList is not None else 0]
    if sensorList is not None:
        values.extend(sensorList)
    
    return database.fetch(query=query, isOne=False, values=values)
   