@echo off
REM Military Base Access Control - Startup Script
REM This script starts the Flask application

echo.
echo ========================================
echo Military Base Access Control System
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if dependencies are installed
echo Checking dependencies...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Start Flask
echo.
echo Starting Flask server...
echo.
python app.py
pause
