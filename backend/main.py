from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

DATABASE = 'flight_booking.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS flights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            flight_number TEXT UNIQUE NOT NULL,
            airline TEXT NOT NULL,
            departure TEXT NOT NULL,
            destination TEXT NOT NULL,
            departure_time TEXT NOT NULL,
            total_seats INTEGER NOT NULL,
            available_seats INTEGER NOT NULL
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            flight_id INTEGER NOT NULL,
            passenger_name TEXT NOT NULL,
            passport_number TEXT NOT NULL,
            is_canceled BOOLEAN DEFAULT FALSE,
            booking_time TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (flight_id) REFERENCES flights (id)
        )
    ''')
    
    conn.commit()
    conn.close()

init_db()

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/flights/', methods=['POST'])
def add_flight():
    try:
        data = request.get_json()
        
        if data['total_seats'] <= 0:
            return jsonify({'error': 'Total seats must be positive'}), 400
        
        conn = get_db_connection()
        c = conn.cursor()
        
        c.execute('''
            INSERT INTO flights (flight_number, airline, departure, destination, departure_time, total_seats, available_seats)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['flight_number'],
            data['airline'],
            data['departure'],
            data['destination'],
            data['departure_time'],
            data['total_seats'],
            data['total_seats']
        ))
        
        flight_id = c.lastrowid
        conn.commit()
        
        c.execute('SELECT * FROM flights WHERE id = ?', (flight_id,))
        flight = dict(c.fetchone())
        conn.close()
        
        return jsonify(flight), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/flights/', methods=['GET'])
def get_flights():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM flights')
    flights = [dict(row) for row in c.fetchall()]
    conn.close()
    return jsonify(flights)

@app.route('/flights/<int:flight_id>', methods=['GET'])
def get_flight(flight_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM flights WHERE id = ?', (flight_id,))
    flight = c.fetchone()
    conn.close()
    
    if not flight:
        return jsonify({'error': 'Flight not found'}), 404
    
    return jsonify(dict(flight))

@app.route('/flights/<int:flight_id>/book', methods=['POST'])
def book_ticket(flight_id):
    try:
        data = request.get_json()
        conn = get_db_connection()
        c = conn.cursor()
        
        c.execute('SELECT * FROM flights WHERE id = ?', (flight_id,))
        flight = c.fetchone()
        
        if not flight:
            conn.close()
            return jsonify({'error': 'Flight not found'}), 404
        
        flight_dict = dict(flight)
        
        if flight_dict['available_seats'] <= 0:
            conn.close()
            return jsonify({'error': 'No seats available'}), 400
        
        if not data.get('passport_number') or len(data['passport_number']) < 5:
            conn.close()
            return jsonify({'error': 'Invalid passport number'}), 400
        
        c.execute('''
            SELECT * FROM bookings 
            WHERE flight_id = ? AND passport_number = ? AND is_canceled = FALSE
        ''', (flight_id, data['passport_number']))
        existing_booking = c.fetchone()
        
        if existing_booking:
            conn.close()
            return jsonify({'error': 'Passport number already used for this flight'}), 400
        
        c.execute('''
            INSERT INTO bookings (flight_id, passenger_name, passport_number)
            VALUES (?, ?, ?)
        ''', (flight_id, data['passenger_name'], data['passport_number']))
        
        booking_id = c.lastrowid
        
        c.execute('''
            UPDATE flights 
            SET available_seats = available_seats - 1 
            WHERE id = ?
        ''', (flight_id,))
        
        conn.commit()
        
        c.execute('SELECT * FROM bookings WHERE id = ?', (booking_id,))
        booking = dict(c.fetchone())
        conn.close()
        
        return jsonify(booking)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/bookings/<int:booking_id>', methods=['DELETE'])
def cancel_booking(booking_id):
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute('SELECT * FROM bookings WHERE id = ?', (booking_id,))
    booking = c.fetchone()
    
    if not booking:
        conn.close()
        return jsonify({'error': 'Booking not found'}), 404
    
    booking_dict = dict(booking)
    
    if booking_dict['is_canceled']:
        conn.close()
        return jsonify({'error': 'Booking already canceled'}), 400
    
    c.execute('''
        UPDATE bookings 
        SET is_canceled = TRUE 
        WHERE id = ?
    ''', (booking_id,))
    
    c.execute('''
        UPDATE flights 
        SET available_seats = available_seats + 1 
        WHERE id = ?
    ''', (booking_dict['flight_id'],))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Booking canceled successfully'})

@app.route('/bookings/', methods=['GET'])
def get_bookings():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM bookings')
    bookings = [dict(row) for row in c.fetchall()]
    conn.close()
    return jsonify(bookings)

@app.route('/')
def home():
    return jsonify({'message': 'Flight Booking System API is running!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)