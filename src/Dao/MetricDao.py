from src.Utils.Database import database
from src.Modals.Metrics import Metrics
from datetime import datetime

def postMetricsDao(metrics: Metrics) -> None:
    query = "INSERT into metrics VALUES (id, :sensorId, :temperature, :humidity, :timestamp)"
    values = {"sensorId": metrics.sensorId, "temperature": metrics.temperature, "humidity": metrics.humidity, "timestamp": datetime.utcnow()}