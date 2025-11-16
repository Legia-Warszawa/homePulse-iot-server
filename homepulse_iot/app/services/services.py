from app.database import (
    SessionLocal,
    ESPRoom1,
    ESPOutside1,
    ESPFurnanceCO2
)
from app.model.iot_devices import ESPRoom1 as PydRoom, ESPOutside_1, ESPFurnanceCO2 as PydFurnace
from app.model.iot_devices import IoTMessageModel


#ZAPIS 

def save_room_data(temperature: float):
    db = SessionLocal()
    try:
        entry = ESPRoom1(temperature=temperature)
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry
    finally:
        db.close()


def save_outside_data(temperature: float, humidity: float, pressure: float):
    db = SessionLocal()
    try:
        entry = ESPOutside1(
            temperature=temperature,
            humidity=humidity,
            pressure=pressure
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry
    finally:
        db.close()


def save_furnance_data(temperature: float):
    db = SessionLocal()
    try:
        entry = ESPFurnanceCO2(temperature=temperature)
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry
    finally:
        db.close()


# ODCZYT OSTATNICH WARTOŚCI

def get_latest_room():
    db = SessionLocal()
    try:
        return db.query(ESPRoom1).order_by(ESPRoom1.timestamp.desc()).first()
    finally:
        db.close()


def get_latest_outside():
    db = SessionLocal()
    try:
        return db.query(ESPOutside1).order_by(ESPOutside1.timestamp.desc()).first()
    finally:
        db.close()


def get_latest_furnance():
    db = SessionLocal()
    try:
        return db.query(ESPFurnanceCO2).order_by(ESPFurnanceCO2.timestamp.desc()).first()
    finally:
        db.close()
        
def get_history(model, limit: int = 100):
    db = SessionLocal()
    try:
        return (
            db.query(model)
            .order_by(model.timestamp.desc())
            .limit(limit)
            .all()
        )
    finally:
        db.close()


def get_latest_message():
    """Zwraca ostatnie dane ze wszystkich urządzeń z bazy SQLite"""

    room = get_latest_room()
    outside = get_latest_outside()
    furnance = get_latest_furnance()

    return {
        "ESP_Room_1": {"temperature": room.temperature} if room else None,
        "ESP_Outside_1": {
            "temperature": outside.temperature,
            "humidity": outside.humidity,
            "pressure": outside.pressure
        } if outside else None,
        "ESP_Furnance_CO_2": {
            "temperature": furnance.temperature
        } if furnance else None,
        "timestamp": room.timestamp if room else None
    }
