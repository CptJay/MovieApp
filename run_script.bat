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

:: Install the required Python dependencies (including requests)
echo Installing dependencies...
pip install -r backend\requirements.txt

:: Run the consume_api.py script
echo Running the consume_api.py script...
python consume_api.py

ENDLOCAL