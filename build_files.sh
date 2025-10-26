#!/bin/bash

# Build the project
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collect static files..."
python manage.py collectstatic --noinput --clear