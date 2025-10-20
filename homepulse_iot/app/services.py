from azure.eventhub import EventHubConsumerClient
import json
import os

# 🔧 Konfiguracja Event Hub
connection_str = os.getenv("EVENTHUB_CONN_STR", "Endpoint=sb://germanywestcentraldedns016.servicebus.windows.net/;SharedAccessKeyName=iothubowner;SharedAccessKey=qj0CrVYargzuemQ7rC3hdsWy1wTdXgjqTAIoTKUKX7w=;EntityPath=iothub-ehub-iotproject-55895460-82dd4e868e")
consumer_group = os.getenv("EVENTHUB_CONSUMER_GROUP", "$Default")

# 🧠 Bufor ostatniej wiadomości
_latest_message = {"status": "brak danych"}

def on_event(partition_context, event):
    global _latest_message
    try:
        data = event.body_as_str()
        print(f"📨 Otrzymano wiadomość: {data}")
        try:
            _latest_message = json.loads(data)
        except json.JSONDecodeError:
            _latest_message = {"raw_data": data}
        partition_context.update_checkpoint(event)
    except Exception as e:
        print(f"❌ Błąd przetwarzania: {e}")

def start_eventhub_listener():
    client = EventHubConsumerClient.from_connection_string(
        connection_str,
        consumer_group=consumer_group
    )
    print("🔊 Nasłuchiwanie danych z Azure IoT Hub rozpoczęte...")
    with client:
        client.receive(on_event=on_event, starting_position="-1")

def get_latest_message():
    return _latest_message
