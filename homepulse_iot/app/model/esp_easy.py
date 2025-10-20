from pydantic import BaseModel
from datetime import datetime

class ESPEasyModel(BaseModel):
    """Model dla urządzenia ESP_Easy (tylko temperatura)"""
    temperature: float
    timestamp: datetime