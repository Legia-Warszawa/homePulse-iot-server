from pydantic import BaseModel
from datetime import datetime

class ESPRoom1(BaseModel):
    """Model dla urządzenia ESPRoom1 (tylko temperatura)"""
    temperature: float
    