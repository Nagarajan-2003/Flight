import pytest
from fastapi.testclient import TestClient
from main import app
import models
import database

client = TestClient(app)

def test_add_flight():
    flight_data = {
        "flight_number": "TEST123",
        "airline": "Test Airlines",
        "departure": "JFK",
        "destination": "LAX",
        "departure_time": "2024-12-01T10:00:00",
        "total_seats": 150
    }
    
    response = client.post("/flights/", json=flight_data)
    assert response.status_code == 201
    assert response.json()["flight_number"] == "TEST123"
    assert response.json()["available_seats"] == 150

def test_book_ticket():
    flight_data = {
        "flight_number": "BOOKTEST",
        "airline": "Test Airlines",
        "departure": "JFK",
        "destination": "LAX",
        "departure_time": "2024-12-01T10:00:00",
        "total_seats": 2
    }
    
    flight_response = client.post("/flights/", json=flight_data)
    flight_id = flight_response.json()["id"]
    
    booking_data = {
        "passenger_name": "John Doe",
        "passport_number": "AB123456"
    }
    
    response = client.post(f"/flights/{flight_id}/book", json=booking_data)
    assert response.status_code == 200
    assert response.json()["passenger_name"] == "John Doe"

def test_overbooking_prevention():
    flight_data = {
        "flight_number": "SMALLTEST",
        "airline": "Test Airlines",
        "departure": "JFK",
        "destination": "LAX",
        "departure_time": "2024-12-01T10:00:00",
        "total_seats": 1
    }
    
    flight_response = client.post("/flights/", json=flight_data)
    flight_id = flight_response.json()["id"]
    
    booking1_data = {
        "passenger_name": "First Passenger",
        "passport_number": "PASS001"
    }
    
    booking2_data = {
        "passenger_name": "Second Passenger",
        "passport_number": "PASS002"
    }
    
    response1 = client.post(f"/flights/{flight_id}/book", json=booking1_data)
    assert response1.status_code == 200
    
    response2 = client.post(f"/flights/{flight_id}/book", json=booking2_data)
    assert response2.status_code == 400

def test_invalid_passport():
    flight_data = {
        "flight_number": "PASSTEST",
        "airline": "Test Airlines",
        "departure": "JFK",
        "destination": "LAX",
        "departure_time": "2024-12-01T10:00:00",
        "total_seats": 10
    }
    
    flight_response = client.post("/flights/", json=flight_data)
    flight_id = flight_response.json()["id"]
    
    booking_data = {
        "passenger_name": "Test Passenger",
        "passport_number": "123"
    }
    
    response = client.post(f"/flights/{flight_id}/book", json=booking_data)
    assert response.status_code == 400