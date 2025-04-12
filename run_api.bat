@echo off
SETLOCAL

:: Check if the virtual environment exists, create it if it doesn't
IF NOT EXIST "backend\.venv" (
    echo Virtual environment not found. Creating one...
    python -m venv backend\.venv
    IF %ERRORLEVEL% NEQ 0 (
        echo Failed to create virtual environment. Make sure Python is installed.
        exit /b 1
    )
)

:: Activate the virtual environment
echo Activating virtual environment...
call backend\.venv\Scripts\activate.bat

:: Install the required Python dependencies
echo Installing dependencies...
pip install -r backend\requirements.txt

:: Run the Flask API server
echo Starting the Flask API...
python backend\app.py

ENDLOCAL