from fastapi import APIRouter, Query
from app.model.iot_devices import IoTMessageModel
from app.services import services as service
from app.database import ESPOutside1, ESPRoom1, ESPFurnanceCO2

router = APIRouter(prefix="/items", tags=["Items"])

# ===== ZAPIS RĘCZNY (POST) =====
@router.post("/esp-pokoj")
def add_room_data(temperature: float):
    return service.save_room_data(temperature)


@router.post("/esp-zewnatrz")
def add_outside_data(temperature: float, humidity: float, pressure: float):
    return service.save_outside_data(temperature, humidity, pressure)


@router.post("/esp-piec")
def add_furnance_data(temperature: float):
    return service.save_furnance_data(temperature)


# ===== ODCZYT OGÓLNY =====
@router.get("/latest", response_model=IoTMessageModel)
def get_latest_iot_message():
    """Zwraca ostatnie dane ze wszystkich urządzeń (SQLite + EventHub)"""
    return service.get_latest_message()


@router.get("/eventhub/raw")
def get_eventhub_raw():
    """Zwraca surową wiadomość z EventHub bufora"""
    return service.get_eventhub_raw_message()


# ===== ODCZYT POSZCZEGÓLNYCH URZĄDZEŃ =====
@router.get("/devices/esp-pokoj")
def get_esp_pokoj_data():
    """Zwraca najnowsze dane z pokoju"""
    room = service.get_latest_room()
    if room:
        return {"temperature": room.temperature, "timestamp": room.timestamp}
    return {"error": "Brak danych z pokoju"}


@router.get("/devices/esp-zewnatrz")
def get_esp_zewnatrz_data():
    """Zwraca najnowsze dane zewnętrzne"""
    outside = service.get_latest_outside()
    if outside:
        return {
            "temperature": outside.temperature,
            "humidity": outside.humidity,
            "pressure": outside.pressure,
            "timestamp": outside.timestamp,
        }
    return {"error": "Brak danych zewnętrznych"}


@router.get("/devices/esp-piec")
def get_esp_piec_data():
    """Zwraca najnowsze dane z pieca"""
    furnace = service.get_latest_furnance()
    if furnace:
        return {"temperature": furnace.temperature, "timestamp": furnace.timestamp}
    return {"error": "Brak danych z pieca"}


# ===== HISTORIA =====
@router.get("/history/esp-pokoj")
def history_esp_pokoj(limit: int = Query(100, gt=0, le=1000)):
    """Historia pomiarów temperatury z pokoju"""
    data = service.get_history(ESPRoom1, limit)
    return [
        {"temperature": row.temperature, "timestamp": row.timestamp}
        for row in data
    ]


@router.get("/history/esp-zewnatrz")
def history_esp_zewnatrz(limit: int = Query(100, gt=0, le=1000)):
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
def history_esp_piec(limit: int = Query(100, gt=0, le=1000)):
    """Historia pomiarów temperatury z pieca"""
    data = service.get_history(ESPFurnanceCO2, limit)
    return [
        {"temperature": row.temperature, "timestamp": row.timestamp}
        for row in data
    ]