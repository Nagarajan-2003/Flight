import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_BASE = 'http://localhost:8000';

function App() {
  const [flights, setFlights] = useState([]);
  const [bookings, setBookings] = useState([]);
  const [selectedFlight, setSelectedFlight] = useState(null);
  const [passengerName, setPassengerName] = useState('');
  const [passportNumber, setPassportNumber] = useState('');
  const [cancelBookingId, setCancelBookingId] = useState('');
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetchFlights();
    fetchBookings();
  }, []);

  const fetchFlights = async () => {
    try {
      const response = await axios.get(`${API_BASE}/flights/`);
      setFlights(response.data);
    } catch (error) {
      setMessage('Error fetching flights');
    }
  };

  const fetchBookings = async () => {
    try {
      const response = await axios.get(`${API_BASE}/bookings/`);
      setBookings(response.data);
    } catch (error) {
      setMessage('Error fetching bookings');
    }
  };

  const handleBookFlight = async (flightId) => {
    if (!passengerName || !passportNumber) {
      setMessage('Please enter passenger name and passport number');
      return;
    }

    try {
      const response = await axios.post(`${API_BASE}/flights/${flightId}/book`, {
        passenger_name: passengerName,
        passport_number: passportNumber
      });
      
      setMessage(`Booking successful! Booking ID: ${response.data.id}`);
      setPassengerName('');
      setPassportNumber('');
      fetchFlights();
      fetchBookings();
    } catch (error) {
      setMessage(error.response?.data?.detail || 'Booking failed');
    }
  };

  const handleCancelBooking = async () => {
    if (!cancelBookingId) {
      setMessage('Please enter booking ID');
      return;
    }

    try {
      await axios.delete(`${API_BASE}/bookings/${cancelBookingId}`);
      setMessage('Booking canceled successfully');
      setCancelBookingId('');
      fetchFlights();
      fetchBookings();
    } catch (error) {
      setMessage(error.response?.data?.detail || 'Cancellation failed');
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Flight Ticket Booking System</h1>
      </header>

      <div className="container">
        {message && (
          <div className="message">
            {message}
          </div>
        )}

        <div className="section">
          <h2>Available Flights</h2>
          <div className="flights-grid">
            {flights.map(flight => (
              <div key={flight.id} className="flight-card">
                <h3>{flight.airline} - {flight.flight_number}</h3>
                <p>{flight.departure} → {flight.destination}</p>
                <p>Departure: {new Date(flight.departure_time).toLocaleString()}</p>
                <p>Available Seats: {flight.available_seats}</p>
                <div className="booking-form">
                  <input
                    type="text"
                    placeholder="Passenger Name"
                    value={passengerName}
                    onChange={(e) => setPassengerName(e.target.value)}
                  />
                  <input
                    type="text"
                    placeholder="Passport Number"
                    value={passportNumber}
                    onChange={(e) => setPassportNumber(e.target.value)}
                  />
                  <button 
                    onClick={() => handleBookFlight(flight.id)}
                    disabled={flight.available_seats === 0}
                  >
                    {flight.available_seats === 0 ? 'No Seats' : 'Book Flight'}
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="section">
          <h2>Cancel Booking</h2>
          <div className="cancel-form">
            <input
              type="text"
              placeholder="Booking ID"
              value={cancelBookingId}
              onChange={(e) => setCancelBookingId(e.target.value)}
            />
            <button onClick={handleCancelBooking}>Cancel Booking</button>
          </div>
        </div>

        <div className="section">
          <h2>All Bookings</h2>
          <div className="bookings-list">
            {bookings.map(booking => (
              <div key={booking.id} className="booking-card">
                <p>Booking ID: {booking.id}</p>
                <p>Passenger: {booking.passenger_name}</p>
                <p>Passport: {booking.passport_number}</p>
                <p>Status: {booking.is_canceled ? 'Canceled' : 'Confirmed'}</p>
                <p>Flight ID: {booking.flight_id}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;