@echo off
REM Check if the virtual environment exists
if exist "backend\.venv" (
    echo Activating virtual environment...
    call backend\.venv\Scripts\activate.bat
) else (
    echo Virtual environment not found. Please make sure you have set up the backend virtual environment.
    exit /b 1
)

REM Install dependencies if necessary
echo Installing dependencies...
pip install -r backend\requirements.txt
pip install requests

REM Run the consume_api.py script
echo Running the consume_api.py script...
python consume_api.py