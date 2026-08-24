import os
from database import Base, engine, get_db
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from models import Booking, Flight
from pydantic import BaseModel
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AeroBook API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class FlightCreate(BaseModel):
    flight_number: str
    origin: str
    destination: str
    departure_time: str
    price: float
    available_seats: int


class BookingCreate(BaseModel):
    passenger_name: str
    passenger_email: str
    flight_id: int
    seats_booked: int


@app.get("/api/flights")
def get_flights(db: Session = Depends(get_db)):
    return db.query(Flight).all()


@app.get("/api/bookings")
def get_bookings(db: Session = Depends(get_db)):
    return db.query(Booking).all()


@app.post("/api/flights")
def create_flight(flight: FlightCreate, db: Session = Depends(get_db)):
    db_flight = Flight(**flight.dict())
    db.add(db_flight)
    db.commit()
    db.refresh(db_flight)
    return db_flight


@app.post("/api/bookings")
def book_flight(booking: BookingCreate, db: Session = Depends(get_db)):
    flight = db.query(Flight).filter(Flight.id == booking.flight_id).first()
    if not flight or flight.available_seats < booking.seats_booked:
        raise HTTPException(
            status_code=400, detail="Flight unavailable or not enough seats"
        )

    flight.available_seats -= booking.seats_booked
    db_booking = Booking(**booking.dict())
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return {"message": "Booking confirmed", "booking": db_booking}


@app.delete("/api/bookings/{booking_id}")
def cancel_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    flight = db.query(Flight).filter(Flight.id == booking.flight_id).first()
    if flight:
        flight.available_seats += booking.seats_booked

    db.delete(booking)
    db.commit()
    return {
        "message": f"Booking #{booking_id} cancelled successfully and seats restored."
    }


frontend_build_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "frontend", "build"
)

if os.path.exists(frontend_build_path):
    app.mount(
        "/static",
        StaticFiles(directory=os.path.join(frontend_build_path, "static")),
        name="static",
    )

    @app.get("/{full_path:path}")
    async def serve_react_app(full_path: str):
        file_path = os.path.join(frontend_build_path, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_build_path, "index.html"))
