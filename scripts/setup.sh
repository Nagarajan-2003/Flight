#!/bin/bash

echo "Setting up Flight Booking System..."

cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cd ../frontend
npm install

echo "Setup completed successfully!"