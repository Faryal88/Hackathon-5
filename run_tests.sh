#!/bin/bash
# Shell script to install dependencies and run complete test suite

echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Failed to install dependencies"
    exit 1
fi

echo "Dependencies installed successfully"

echo "Running complete test suite..."
python3 run_complete_test_suite.py