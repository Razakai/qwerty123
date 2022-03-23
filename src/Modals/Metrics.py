from pydantic import BaseModel


class Metrics(BaseModel):
    sensor_id: str
    temperature: float
    humidity: float
