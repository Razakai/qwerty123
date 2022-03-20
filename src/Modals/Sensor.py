from typing import Optional
from pydantic import BaseModel


class Sensor(BaseModel):
    id: str
    country: Optional[str] = None
    city: Optional[str] = None