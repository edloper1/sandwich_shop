#!/bin/bash

# Build the project
echo "Creating virtual environment..."
python3.9 -m venv python3-virtualenv
source python3-virtualenv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collect static files..."
python manage.py collectstatic --noinput --clear