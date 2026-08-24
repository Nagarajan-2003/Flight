import os
from database import Base, SessionLocal, engine
from models import Booking, Flight

# Recreate tables so new columns are properly initialized
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    if db.query(Flight).count() == 0:
        sample_flights = [
            Flight(
                flight_number="AA101",
                origin="New York",
                destination="London",
                departure_time="10:00 AM",
                price=450.0,
                available_seats=20,
            ),
            Flight(
                flight_number="BA202",
                origin="London",
                destination="Tokyo",
                departure_time="02:30 PM",
                price=680.0,
                available_seats=15,
            ),
            Flight(
                flight_number="DL303",
                origin="San Francisco",
                destination="Paris",
                departure_time="08:15 PM",
                price=520.0,
                available_seats=10,
            ),
        ]
        db.add_all(sample_flights)
        db.commit()
        print("Database seeded with sample flights.")
finally:
    db.close()
