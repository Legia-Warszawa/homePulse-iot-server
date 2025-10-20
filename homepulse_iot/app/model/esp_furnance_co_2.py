from pydantic import BaseModel
from datetime import datetime

class ESPFurnanceCO2(BaseModel):
    """Model dla urządzenia ESP_Furnance_CO2 (tylko temperatura)"""
    temperature: float
   