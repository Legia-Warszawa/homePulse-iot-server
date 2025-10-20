from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

from .esp_easy import ESPEasyModel
from .esp_easy1 import ESPEasy1Model
from .esp_esap2 import ESPEasy2Model


class IoTMessageModel(BaseModel):
    """Główny model dla wszystkich wiadomości IoT"""
    status: Dict[str, Any] = {}
    ESP_Easy: Optional[ESPEasyModel] = None
    ESP_Easy_1: Optional[ESPEasy1Model] = None
    ESP_Easy_2: Optional[ESPEasy2Model] = None
    timestamp: Optional[datetime] = None
