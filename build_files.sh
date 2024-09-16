#!/bin/bash

# Set up Python environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run Django build commands or any other setup steps
python manage.py collectstatic --noinput
python manage.py migrate
