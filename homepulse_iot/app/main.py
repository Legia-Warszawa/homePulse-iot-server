from fastapi import FastAPI, HTTPException
from threading import Thread
from sqlalchemy import text
from app.services.services import start_eventhub_listener
from app.routes import items
from app.database import engine, Base

app = FastAPI(title="Azure IoT Hub FastAPI Server")

app.include_router(items.router)

@app.on_event("startup")
async def startup_event():
    try:
        # Test SQLite
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ SQLite połączenie OK")
        
        # Utwórz tabele
        Base.metadata.create_all(bind=engine)
        print("✅ Tabele utworzone")
        
        # EventHub
        thread = Thread(target=start_eventhub_listener, daemon=True)
        thread.start()
        print("🚀 EventHub uruchomiony")
        
    except Exception as e:
        print(f"❌ Błąd: {e}")

@app.get("/")
def root():
    return {"message": "FastAPI działa", "database": "SQLite"}

@app.get("/health")
def health():
    return {"status": "OK", "database": "SQLite"}