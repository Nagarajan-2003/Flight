from flight_sdk.api.flights_api import FlightsApi
from flight_sdk import ApiClient
from flight_sdk.models.flight_create import FlightCreate
from flight_sdk.models.booking_create import BookingCreate
from datetime import datetime

client = ApiClient()
flights_api = FlightsApi(client)

flights = flights_api.get_flights()
print("Available flights:", flights)

new_flight = FlightCreate(
    flight_number="SDK123",
    airline="SDK Airlines",
    departure="JFK",
    destination="SFO",
    departure_time=datetime(2024, 12, 1, 14, 30, 0),
    total_seats=100
)

added_flight = flights_api.add_flight(new_flight)
print("Added flight:", added_flight)

booking_data = BookingCreate(
    passenger_name="SDK User",
    passport_number="SDK123456"
)

booking = flights_api.book_ticket(added_flight.id, booking_data)
print("Booking created:", booking)