from azure.eventhub import EventHubConsumerClient

connection_str = "Endpoint=sb://germanywestcentraldedns016.servicebus.windows.net/;SharedAccessKeyName=iothubowner;SharedAccessKey=qj0CrVYargzuemQ7rC3hdsWy1wTdXgjqTAIoTKUKX7w=;EntityPath=iothub-ehub-iotproject-55895460-82dd4e868e"
consumer_group = "$Default"  # lub inna grupa zdefiniowana w IoT Hub

def on_event(partition_context, event):
    print("🔹 Otrzymano wiadomość:")
    print(event.body_as_str())
    # potwierdzenie odczytu (opcjonalne)
    partition_context.update_checkpoint(event)

client = EventHubConsumerClient.from_connection_string(
    connection_str,
    consumer_group=consumer_group
)

print("Nasłuchuję danych z IoT Hub Event Hub endpoint...")
try:
    with client:
        client.receive(on_event=on_event, starting_position="-1")
except KeyboardInterrupt:
    print("\n❌ Zatrzymano nasłuchiwanie")
except Exception as e:
    print(f"❌ Błąd: {e}")