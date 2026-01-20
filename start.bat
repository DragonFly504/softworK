@echo off
:: TTCP Worldwide - Quick Start Script (Windows)
title TTCP Worldwide Tracking System

echo.
echo ========================================
echo   TTCP Worldwide Tracking System
echo ========================================
echo.

:: Navigate to project directory
cd /d "%~dp0"

:: Set Python path to virtual environment
set VENV_PYTHON=%~dp0venv\Scripts\python.exe

:: Check if virtual environment exists
if not exist "%VENV_PYTHON%" (
    echo [!] No virtual environment found. Creating one...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        echo Make sure Python is installed.
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
    
    echo [*] Installing dependencies...
    "%VENV_PYTHON%" -m pip install --upgrade pip
    "%VENV_PYTHON%" -m pip install Django python-dotenv requests
    echo [OK] Dependencies installed
)

echo [*] Applying database migrations...
"%VENV_PYTHON%" manage.py migrate --run-syncdb

echo.
echo ========================================
echo   Server Ready!
echo ========================================
echo.
echo   Website:     http://127.0.0.1:8000
echo   Admin Panel: http://127.0.0.1:8000/admin/
echo   Tracking:    http://127.0.0.1:8000/track/
echo.
echo   Press Ctrl+C to stop the server
echo ========================================
echo.

:: Start the server using venv Python directly
"%VENV_PYTHON%" manage.py runserver

pause
