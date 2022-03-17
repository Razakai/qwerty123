from typing import Optional
from pydantic import BaseModel


class Metrics(BaseModel):
    sensorId: int
    temperature: float
    humidity: float