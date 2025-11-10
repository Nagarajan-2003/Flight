#!/bin/bash

echo "Starting Flight Booking System..."

cd backend
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 &

cd ../frontend
npm start &

echo "System started! Backend: http://localhost:8000, Frontend: http://localhost:3000"