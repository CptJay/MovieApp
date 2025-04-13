#!/bin/bash

# Move into the frontend directory
cd frontend || { echo "Frontend directory not found!"; exit 1; }

# Check if node_modules exists, if not install dependencies
if [ ! -d "node_modules" ]; then
    echo "Installing React frontend dependencies..."
    npm install
fi

# Start the React development server
echo "Starting React frontend..."
npm start