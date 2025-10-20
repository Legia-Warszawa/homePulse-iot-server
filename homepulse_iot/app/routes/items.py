from fastapi import APIRouter
from app.model.iot_devices import IoTMessageModel
from app.services import get_latest_message

router = APIRouter(prefix="/items", tags=["Items"])

@router.get("/latest", response_model=IoTMessageModel)
def get_latest_iot_message():
    """Zwraca ostatnią wiadomość IoT z wszystkimi urządzeniami"""
    raw_message = get_latest_message()
    return IoTMessageModel(**raw_message)

@router.get("/devices/esp-pokoj")
def get_esp_pokoj_data():
    """Zwraca dane z pokoju ESP_Pokoj_1"""
    message = get_latest_message()
    if "ESP_Pokoj_1" in message:
        return message["ESP_Pokoj_1"]
    return {"error": "Brak danych z ESP_Pokoj_1"}

@router.get("/devices/esp-zewnatrz")
def get_esp_zewnatrz_data():
    """Zwraca dane zewnętrzne ESP_Zewnatrz_1"""
    message = get_latest_message()
    if "ESP_Zewnatrz_1" in message:
        return message["ESP_Zewnatrz_1"]
    return {"error": "Brak danych z ESP_Zewnatrz_1"}

@router.get("/devices/esp-piec")
def get_esp_piec_data():
    """Zwraca dane z pieca ESP_Piec_CO_2"""
    message = get_latest_message()
    if "ESP_Piec_CO_2" in message:
        return message["ESP_Piec_CO_2"]
    return {"error": "Brak danych z ESP_Piec_CO_2"}