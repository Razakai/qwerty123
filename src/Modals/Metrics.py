from typing import Optional
from pydantic import BaseModel


class Metrics(BaseModel):
    sensor_id: int
    temperature: float
    humidity: float