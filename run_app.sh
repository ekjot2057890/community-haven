#!/bin/bash

# Set up Python virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install required packages
echo "Installing dependencies..."
pip install -r requirements.txt

# Set necessary environment variables
export FLASK_APP=backend/App/run.py
export FLASK_ENV=development
export MONGO_URI="mongodb://localhost:27017/community_pulse"
export JWT_SECRET_KEY="development-secret-key"

# Run the Flask application
echo "Starting Flask application..."
cd backend
python3 -m flask run --host=0.0.0.0

# Deactivate virtual environment when the application stops
deactivate 