#!/bin/bash

# Check if the virtual environment exists, and activate it
if [ -d "backend/.venv" ]; then
    echo "Activating virtual environment..."
    source backend/.venv/Scripts/activate  # On Windows, use 'backend\.venv\Scripts\activate'
else
    echo "Virtual environment not found. Please make sure you have set up the backend virtual environment."
    exit 1
fi

# Install the required Python dependencies (including requests)
echo "Installing dependencies..."
pip install -r backend/requirements.txt

# Install 'requests' if it's not already included in your requirements.txt
pip install requests

# Run the consume_api.py script
echo "Running the consume_api.py script..."
python consume_api.py