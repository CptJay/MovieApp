#!/bin/bash

# Check if the virtual environment exists, and activate it
if [ -d "backend/.venv" ]; then
    echo "Activating virtual environment..."
    source backend/.venv/Scripts/activate  # On Windows, use 'backend\.venv\Scripts\activate'
else
    echo "Virtual environment not found. Please make sure you have set up the backend virtual environment."
    exit 1
fi

# Install the required Python dependencies
echo "Installing dependencies..."
pip install -r backend/requirements.txt

# Run the Flask API server
echo "Starting the Flask API..."
python backend/app.py