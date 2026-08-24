import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [flights, setFlights] = useState([]);
  const [bookings, setBookings] = useState([]);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [selectedFlight, setSelectedFlight] = useState(null);
  const [seats, setSeats] = useState(1);
  const [status, setStatus] = useState('');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [flightsRes, bookingsRes] = await Promise.all([
        fetch('/api/flights'),
        fetch('/api/bookings')
      ]);
      const flightsData = await flightsRes.json();
      const bookingsData = await bookingsRes.json();
      setFlights(flightsData);
      setBookings(bookingsData);
    } catch (err) {
      console.error('Error fetching data:', err);
    }
  };

  const handleBooking = async (e) => {
    e.preventDefault();
    if (!selectedFlight) {
      setStatus('Please select a flight to book.');
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
        setStatus(`Booking Confirmed! (ID: #${data.booking.id})`);
        setName('');
        setEmail('');
        setSeats(1);
        setSelectedFlight(null);
        loadData();
      } else {
        setStatus(`Error: ${data.detail || 'Failed to book'}`);
      }
    } catch (err) {
      setStatus('Booking request failed.');
    }
  };

  const handleCancelBooking = async (bookingId) => {
    try {
      const res = await fetch(`/api/bookings/${bookingId}`, {
        method: 'DELETE',
      });
      const data = await res.json();
      if (res.ok) {
        setStatus(data.message);
        loadData();
      } else {
        setStatus(`Error: ${data.detail || 'Failed to cancel booking'}`);
      }
    } catch (err) {
      setStatus('Cancellation request failed.');
    }
  };

  return (
    <div className="container">
      <h1>AeroBook</h1>
      {status && <div className="status-box">{status}</div>}

      <div className="grid">
        <div className="card">
          <h2>1. Available Flights</h2>
          {flights.map((f) => (
            <div
              key={f.id}
              className={`flight-item ${selectedFlight?.id === f.id ? 'active' : ''}`}
              onClick={() => setSelectedFlight(f)}
            >
              <strong>{f.flight_number}</strong>: {f.origin} &rarr; {f.destination}
              <br />
              <span>Time: {f.departure_time} | Seats Left: {f.available_seats} | ${f.price}</span>
            </div>
          ))}
        </div>

        <div className="card">
          <h2>2. Reserve Seats</h2>
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
            <button type="submit" disabled={!selectedFlight}>
              {selectedFlight ? `Book ${selectedFlight.flight_number}` : 'Select a Flight Above'}
            </button>
          </form>
        </div>
      </div>

      <div className="card full-width">
        <h2>3. Manage Bookings & Cancellations</h2>
        {bookings.length === 0 ? (
          <p className="no-data">No active bookings found.</p>
        ) : (
          <div className="bookings-list">
            {bookings.map((b) => {
              const bookedFlight = flights.find((f) => f.id === b.flight_id);
              return (
                <div key={b.id} className="booking-item">
                  <div>
                    <strong>Booking #{b.id}</strong> — {b.passenger_name} ({b.passenger_email})
                    <br />
                    <span>
                      Flight: {bookedFlight ? bookedFlight.flight_number : `ID: ${b.flight_id}`} | Seats: {b.seats_booked}
                    </span>
                  </div>
                  <button
                    className="cancel-btn"
                    onClick={() => handleCancelBooking(b.id)}
                  >
                    Cancel Ticket
                  </button>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
