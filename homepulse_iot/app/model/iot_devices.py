from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

from .esp_room_1 import ESPRoom1
from .esp_outside_1 import ESPOutside_1
from .esp_furnance_co_2 import ESPFurnanceCO2


class IoTMessageModel(BaseModel):
    """Główny model dla wszystkich wiadomości IoT"""
    status: Dict[str, Any] = {}
    ESP_Room_1: Optional[ESPRoom1] = Field(None, alias="ESP_Pokoj_1")
    ESP_Outside: Optional[ESPOutside_1] = Field(None, alias="ESP_Zewnatrz_1")
    ESP_Furnance_CO: Optional[ESPFurnanceCO2] = Field(None, alias="ESP_Piec_CO_2")
    timestamp: Optional[datetime] = Field(default_factory=datetime.now)
    
    class Config:
        allow_population_by_field_name = True