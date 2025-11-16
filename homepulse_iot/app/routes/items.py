from fastapi import APIRouter
from app.model.iot_devices import IoTMessageModel
from app.services.services import get_latest_message
from app.services import services as service

router = APIRouter(prefix="/items", tags=["Items"])

@router.post("/esp-pokoj")
def add_room_data(temperature: float):
    return service.save_room_data(temperature)

@router.post("/esp-zewnatrz")
def add_outside_data(temperature: float, humidity: float, pressure: float):
    return service.save_outside_data(temperature, humidity, pressure)

@router.post("/esp-piec")
def add_furnance_data(temperature: float):
    return service.save_furnance_data(temperature)

@router.get("/latest", response_model=IoTMessageModel)
def get_latest_iot_message():
    """Zwraca ostatnią wiadomość IoT z wszystkimi urządzeniami"""
    raw_message = get_latest_message()
    return IoTMessageModel(**raw_message)

@router.get("/devices/esp-pokoj")
def get_esp_pokoj_data():
    """Zwraca dane z pokoju"""
    message = get_latest_message()
    if "ESP_Pokoj_1" in message:
        return message["ESP_Pokoj_1"]
    return {"error": "Brak danych z ESP_Pokoj_1"}