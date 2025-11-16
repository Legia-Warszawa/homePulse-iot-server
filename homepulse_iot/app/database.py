import os
from sqlalchemy import create_engine, Column, Integer, Float, DateTime  # type: ignore[import]
from sqlalchemy.orm import declarative_base, sessionmaker  # type: ignore[import]
from datetime import datetime

# UŻYWAMY SQLite - żadnych serwerów, żadnych haseł!
DATABASE_URL = "sqlite:///./iot_data.db"

engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class ESPRoom1(Base):
    __tablename__ = "esp_room_1"
    
    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class ESPOutside1(Base):
    __tablename__ = "esp_outside_1"
    
    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    pressure = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class ESPFurnanceCO2(Base):
    __tablename__ = "esp_furnance_co_2"
    
    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)