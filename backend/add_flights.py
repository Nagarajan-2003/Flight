import requests
import json

BASE_URL = "http://localhost:8000"

flights = [
    {
        "flight_number": "AA123",
        "airline": "American Airlines", 
        "departure": "New York",
        "destination": "Los Angeles",
        "departure_time": "2024-12-01T10:00:00",
        "total_seats": 150
    },
    {
        "flight_number": "UA456", 
        "airline": "United Airlines",
        "departure": "Chicago",
        "destination": "Miami",
        "departure_time": "2024-12-02T14:30:00",
        "total_seats": 200
    },
    {
        "flight_number": "DL789",
        "airline": "Delta Airlines",
        "departure": "Atlanta", 
        "destination": "Seattle",
        "departure_time": "2024-12-03T09:15:00",
        "total_seats": 180
    }
]

for flight in flights:
    try:
        response = requests.post(f"{BASE_URL}/flights/", json=flight)
        if response.status_code == 201:
            print(f"✅ Added flight {flight['flight_number']}")
        else:
            print(f"❌ Failed to add {flight['flight_number']}: {response.text}")
    except Exception as e:
        print(f"❌ Error adding {flight['flight_number']}: {e}")

print("\n🎉 All flights added! Refresh your frontend at http://localhost:3000")