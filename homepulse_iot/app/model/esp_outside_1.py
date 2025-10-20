from pydantic import BaseModel
from datetime import datetime

class ESPOutside_1(BaseModel):
    """Model dla urządzenia ESP_Outside_1 (temperatura, wilgotność, ciśnienie)"""
    temperature: float
    humidity: float
    pressure: float
    