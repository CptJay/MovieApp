#!/bin/bash

# Check if the virtual environment exists, create it if it doesn't
if [ ! -d "backend/.venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python -m venv backend/.venv

    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment. Make sure Python is installed."
        exit 1
    fi
fi

# Activate the virtual environment
echo "Activating virtual environment..."
# Detect platform and use appropriate activate script
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source backend/.venv/Scripts/activate
else
    source backend/.venv/bin/activate
fi

# Install the required Python dependencies (including requests)
echo "Installing dependencies..."
pip install -r backend/requirements.txt

# Run the consume_api.py script
echo "Running the consume_api.py script..."
python consume_api.py
