from fastapi import FastAPI
from threading import Thread
from app.services import start_eventhub_listener
from app.routes import items

app = FastAPI(title="Azure IoT Hub FastAPI Server")

app.include_router(items.router)

# 🔄 Uruchomienie nasłuchu w tle
@app.on_event("startup")
def startup_event():
    thread = Thread(target=start_eventhub_listener, daemon=True)
    thread.start()
    print("🚀 Wątek nasłuchiwania EventHub uruchomiony!")

@app.get("/")
def root():
    return {"message": "FastAPI działa — nasłuch Azure IoT Hub aktywny"}