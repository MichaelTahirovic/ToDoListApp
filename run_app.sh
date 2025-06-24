#!/bin/bash

echo "Starting To-Do List Application..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

# Check if main.py exists
if [ ! -f "main.py" ]; then
    echo "Error: main.py not found in current directory"
    exit 1
fi

# Try to run the application
echo "Launching application..."
python3 main.py

# If there's an error, show installation instructions
if [ $? -ne 0 ]; then
    echo
    echo "Error running the application. Trying to install dependencies..."
    python3 install.py
    echo
    echo "Trying to run the application again..."
    python3 main.py
fi 