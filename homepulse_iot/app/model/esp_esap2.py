from pydantic import BaseModel
from datetime import datetime

class ESPEasy2Model(BaseModel):
    """Model dla urządzenia ESP_Easy (tylko temperatura)"""
    temperature: float
    timestamp: datetime