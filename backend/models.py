from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class Flight(Base):
    __tablename__ = "flights"
    
    id = Column(Integer, primary_key=True, index=True)
    flight_number = Column(String, unique=True, index=True)
    airline = Column(String)
    departure = Column(String)
    destination = Column(String)
    departure_time = Column(DateTime)
    total_seats = Column(Integer)
    available_seats = Column(Integer)
    
    bookings = relationship("Booking", back_populates="flight")

class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    flight_id = Column(Integer, ForeignKey("flights.id"))
    passenger_name = Column(String)
    passport_number = Column(String)
    is_canceled = Column(Boolean, default=False)
    booking_time = Column(DateTime, default=datetime.utcnow)
    
    flight = relationship("Flight", back_populates="bookings")

class FlightCreate(BaseModel):
    flight_number: str
    airline: str
    departure: str
    destination: str
    departure_time: datetime
    total_seats: int

class FlightResponse(BaseModel):
    id: int
    flight_number: str
    airline: str
    departure: str
    destination: str
    departure_time: datetime
    total_seats: int
    available_seats: int

    class Config:
        from_attributes = True

class BookingCreate(BaseModel):
    passenger_name: str
    passport_number: str

class BookingResponse(BaseModel):
    id: int
    flight_id: int
    passenger_name: str
    passport_number: str
    is_canceled: bool
    booking_time: datetime

    class Config:
        from_attributes = True