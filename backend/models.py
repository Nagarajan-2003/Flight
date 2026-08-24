from database import Base
from sqlalchemy import Column, Float, Integer, String


class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)
    flight_number = Column(String, unique=True, index=True)
    origin = Column(String, index=True)
    destination = Column(String, index=True)
    departure_time = Column(String)
    price = Column(Float)
    available_seats = Column(Integer)


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    passenger_name = Column(String)
    passenger_email = Column(String)
    flight_id = Column(Integer)
    seats_booked = Column(Integer)
