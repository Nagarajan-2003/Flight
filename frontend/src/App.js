import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [flights, setFlights] = useState([]);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [selectedFlight, setSelectedFlight] = useState(null);
  const [seats, setSeats] = useState(1);
  const [status, setStatus] = useState('');

  useEffect(() => {
    fetchFlights();
  }, []);

  const fetchFlights = async () => {
    try {
      const res = await fetch('/api/flights');
      const data = await res.json();
      setFlights(data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleBooking = async (e) => {
    e.preventDefault();
    if (!selectedFlight) {
      setStatus('Please select a flight.');
      return;
    }

    try {
      const res = await fetch('/api/bookings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          passenger_name: name,
          passenger_email: email,
          flight_id: selectedFlight.id,
          seats_booked: parseInt(seats),
        }),
      });

      const data = await res.json();
      if (res.ok) {
        setStatus(`Booking Confirmed! Flight: ${selectedFlight.flight_number}`);
        fetchFlights();
      } else {
        setStatus(`Error: ${data.detail || 'Failed to book'}`);
      }
    } catch (err) {
      setStatus('Booking request failed.');
    }
  };

  return (
    <div className="container">
      <h1>Flight Booking System</h1>
      {status && <div className="status-box">{status}</div>}

      <div className="grid">
        <div className="card">
          <h2>Available Flights</h2>
          {flights.map((f) => (
            <div
              key={f.id}
              className={`flight-item ${selectedFlight?.id === f.id ? 'active' : ''}`}
              onClick={() => setSelectedFlight(f)}
            >
              <strong>{f.flight_number}</strong>: {f.origin} &rarr; {f.destination}
              <br />
              <span>Time: {f.departure_time} | Seats: {f.available_seats} | ${f.price}</span>
            </div>
          ))}
        </div>

        <div className="card">
          <h2>Reserve Seats</h2>
          <form onSubmit={handleBooking}>
            <input
              type="text"
              placeholder="Passenger Name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
            <input
              type="email"
              placeholder="Passenger Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <input
              type="number"
              min="1"
              max="10"
              value={seats}
              onChange={(e) => setSeats(e.target.value)}
              required
            />
            <button type="submit" disabled={!selectedFlight}>Confirm Booking</button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default App;
