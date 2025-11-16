from fastapi import APIRouter, Query  # Dodaj Query
from app.model.iot_devices import IoTMessageModel
from app.services import services as service
from app.database import ESPOutside1, ESPRoom1, ESPFurnanceCO2  # Popraw import

router = APIRouter(prefix="/items", tags=["Items"])


#ZAPIS
@router.post("/esp-pokoj")
def add_room_data(temperature: float):
    return service.save_room_data(temperature)


@router.post("/esp-zewnatrz")
def add_outside_data(temperature: float, humidity: float, pressure: float):
    return service.save_outside_data(temperature, humidity, pressure)


@router.post("/esp-piec")
def add_furnance_data(temperature: float):
    return service.save_furnance_data(temperature)


# ODCZYT
@router.get("/latest", response_model=IoTMessageModel)
def get_latest_iot_message():
    return service.get_latest_message()


#historia 
@router.get("/history/esp-pokoj")  # <-- To brakowało!
def history_esp_pokoj(limit: int = Query(100, gt=0, le=1000, description="Maksymalnie 1000 rekordów")):
    """Historia pomiarów temperatury z pokoju"""
    data = service.get_history(ESPRoom1, limit)
    return [
        {"temperature": row.temperature, "timestamp": row.timestamp}
        for row in data
    ]


@router.get("/history/esp-zewnatrz")
def history_esp_zewnatrz(limit: int = Query(100, gt=0, le=1000, description="Maksymalnie 1000 rekordów")):
    """Historia pomiarów temperatury, wilgotności i ciśnienia z zewnątrz"""
    data = service.get_history(ESPOutside1, limit)
    return [
        {
            "temperature": row.temperature,
            "humidity": row.humidity,
            "pressure": row.pressure,
            "timestamp": row.timestamp,
        }
        for row in data
    ]


@router.get("/history/esp-piec")
def history_esp_piec(limit: int = Query(100, gt=0, le=1000, description="Maksymalnie 1000 rekordów")):
    """Historia pomiarów temperatury z pieca"""  # <-- DODAJ TĘ LINIĘ
    data = service.get_history(ESPFurnanceCO2, limit)
    return [
        {"temperature": row.temperature, "timestamp": row.timestamp}
        for row in data
    ]