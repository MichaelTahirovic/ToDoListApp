@echo off
echo Starting To-Do List Application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from https://python.org
    pause
    exit /b 1
)

REM Check if main.py exists
if not exist "main.py" (
    echo Error: main.py not found in current directory
    pause
    exit /b 1
)

REM Try to run the application
echo Launching application...
python main.py

REM If there's an error, show installation instructions
if errorlevel 1 (
    echo.
    echo Error running the application. Trying to install dependencies...
    python install.py
    echo.
    echo Trying to run the application again...
    python main.py
)

pause 