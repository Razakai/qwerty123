from src.Dao.MetricDao import postMetricsDao
from src.Modals.Metrics import Metrics
from src.Service.SensorService import getSensorService

def postMetricsService(metrics: Metrics) -> None:
    if getSensorService(metrics.sensorId):
        postMetricsDao(metrics)