from fastapi import APIRouter
from app.services import get_latest_message

router = APIRouter(prefix="/items", tags=["Items"])

from fastapi import APIRouter
from app.model.iot_devices import  IoTMessageModel
from app.services import get_latest_message

router = APIRouter(prefix="/items", tags=["Items"])

@router.get("/latest", response_model=IoTMessageModel)
def get_latest_iot_message():
    """Zwraca ostatnią wiadomość IoT z wszystkimi urządzeniami"""
    raw_message = get_latest_message()
    return IoTMessageModel(**raw_message)

@router.get("/devices/esp-easy")
def get_esp_easy_data():
    """Zwraca dane tylko z urządzenia ESP_Easy"""
    message = get_latest_message()
    if "ESP_Easy" in message:
        return message["ESP_Easy"]
    return {"error": "Brak danych z ESP_Easy"}