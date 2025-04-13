@echo off
cd frontend

:: Check if node_modules folder exists
if not exist node_modules (
    echo Installing React frontend dependencies...
    call npm install
)

echo Starting React frontend...
call npm start
