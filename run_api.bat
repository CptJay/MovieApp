@echo off
REM Check if the virtual environment exists
if exist "backend\.venv" (
    echo Activating virtual environment...
    call backend\.venv\Scripts\activate.bat
) else (
    echo Virtual environment not found. Please make sure you have set up the backend virtual environment.
    exit /b 1
)

REM Install dependencies
echo Installing dependencies...
pip install -r backend\requirements.txt

REM Run the Flask API
echo Running the API...
python backend\app.py