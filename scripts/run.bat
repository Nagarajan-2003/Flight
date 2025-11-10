@echo off
echo Starting Flight Booking System...

start cmd /k "cd backend && venv\Scripts\activate && uvicorn main:app --host 0.0.0.0 --port 8000"
timeout /t 5
start cmd /k "cd frontend && npm start"

echo System started! Backend: http://localhost:8000, Frontend: http://localhost:3000
pause