@echo off
echo Setting up Flight Booking System...

cd backend
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt

cd ..\frontend
npm install

echo Setup completed successfully!
pause