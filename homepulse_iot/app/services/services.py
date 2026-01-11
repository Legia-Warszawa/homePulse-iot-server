import os
import json
from threading import Thread
from azure.eventhub import EventHubConsumerClient 
from app.database import (
    SessionLocal,
    ESPRoom1,
    ESPOutside1,
    ESPFurnanceCO2
)
from app.model.iot_devices import ESPRoom1 as PydRoom, ESPOutside_1, ESPFurnanceCO2 as PydFurnace
from app.model.iot_devices import IoTMessageModel

# EventHub konfiguracja
connection_str = os.getenv("EVENTHUB_CONN_STR", "Endpoint=sb://germanywestcentraldedns016.servicebus.windows.net/;SharedAccessKeyName=iothubowner;SharedAccessKey=qj0CrVYargzuemQ7rC3hdsWy1wTdXgjqTAIoTKUKX7w=;EntityPath=iothub-ehub-iotproject-55895460-82dd4e868e")
consumer_group = os.getenv("EVENTHUB_CONSUMER_GROUP", "$Default")

# 🧠 Bufor ostatniej wiadomości
_latest_message = {"status": "brak danych EventHub"} 

# ...existing code...
def get_history_by_date(model, date_str: str, limit: int = 1000):
    """
    Zwraca rekordy dla modelu w przedziale [date 00:00:00, date+1 00:00:00).
    date_str powinien być w formacie YYYY-MM-DD.
    """
    from datetime import datetime, timedelta, time
    try:
        date = datetime.fromisoformat(date_str).date()
    except Exception:
        raise ValueError("Nieprawidłowy format daty. Użyj YYYY-MM-DD")
    start = datetime.combine(date, time.min)
    end = start + timedelta(days=1)

    db = SessionLocal()
    try:
        return (
            db.query(model)
            .filter(model.timestamp >= start, model.timestamp < end)
            .order_by(model.timestamp.desc())
            .limit(limit)
            .all()
        )
    finally:
        db.close()
# ...existing code...

def on_event(partition_context, event):
    global _latest_message
    try:
        data = event.body_as_str()
        print(f"📨 Otrzymano wiadomość: {data}")
        
        try:
            message_data = json.loads(data)
            _latest_message = message_data
            
            # 💾 AUTOMATYCZNY ZAPIS DO SQLITE
            save_eventhub_data_to_sqlite(message_data)
            
        except json.JSONDecodeError:
            _latest_message = {"raw_data": data, "error": "JSON decode error"}
            
        partition_context.update_checkpoint(event)
    except Exception as e:
        print(f"❌ Błąd przetwarzania EventHub: {e}")

def save_eventhub_data_to_sqlite(data):
    """Zapisuje dane z EventHub automatycznie do SQLite"""
    try:
        # Zapisz dane z pokoju
        if "ESP_Pokoj_1" in data and "temperature" in data["ESP_Pokoj_1"]:
            temp = data["ESP_Pokoj_1"]["temperature"]
            save_room_data(temp)
            print(f"✅ SQLite: Pokój {temp}°C")
        
        # Zapisz dane zewnętrzne
        if "ESP_Zewnatrz_1" in data:
            esp_data = data["ESP_Zewnatrz_1"]
            if all(key in esp_data for key in ["temperature", "humidity", "pressure"]):
                save_outside_data(
                    esp_data["temperature"],
                    esp_data["humidity"], 
                    esp_data["pressure"]
                )
                print(f"✅ SQLite: Zewnątrz {esp_data['temperature']}°C, {esp_data['humidity']}%, {esp_data['pressure']}hPa")
        
        # Zapisz dane z pieca
        if "ESP_Piec_CO_2" in data and "temperature" in data["ESP_Piec_CO_2"]:
            temp = data["ESP_Piec_CO_2"]["temperature"]
            save_furnance_data(temp)
            print(f"✅ SQLite: Piec {temp}°C")
            
    except Exception as e:
        print(f"❌ Błąd zapisu do SQLite: {e}")

def start_eventhub_listener():
    """Uruchamia nasłuchiwanie EventHub"""
    try:
        client = EventHubConsumerClient.from_connection_string(
            connection_str,
            consumer_group=consumer_group
        )
        print("🔊 Nasłuchiwanie danych z Azure IoT Hub rozpoczęte...")
        with client:
            client.receive(on_event=on_event, starting_position="-1")
    except Exception as e:
        print(f"❌ Błąd EventHub: {e}")


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
def get_eventhub_raw_message():
    """Zwraca surową wiadomość z EventHub bufora"""
    return _latest_message
