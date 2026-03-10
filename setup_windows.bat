@echo off
REM VentureLens AI - Windows Setup Script
REM Run this from the venturelens directory

echo.
echo ====================================================
echo   VentureLens AI - Setup
echo ====================================================
echo.

REM Check Python version
python --version
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.12+
    exit /b 1
)

REM Create virtual environment
echo [1/5] Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

REM Upgrade pip
echo [2/5] Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo [3/5] Installing dependencies...
pip install -r requirements.txt

REM Copy env file
echo [4/5] Setting up environment...
if not exist .env (
    copy .env.example .env
    echo .env file created. Please edit it with your API keys.
)

REM Run migrations
echo [5/5] Running migrations...
python manage.py migrate

echo.
echo ====================================================
echo   Setup complete!
echo.
echo   Next steps:
echo   1. Edit .env and add your GROQ_API_KEY
echo   2. Run: python manage.py runserver
echo   3. Open: http://localhost:8000
echo ====================================================
echo.
