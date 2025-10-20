from pydantic import BaseModel
from datetime import datetime

class ESPEasy1Model(BaseModel):
    """Model dla urządzenia ESP_Easy_1 (temperatura, wilgotność, ciśnienie)"""
    temperature: float
    humidity: float
    pressure: float
    timestamp: datetime