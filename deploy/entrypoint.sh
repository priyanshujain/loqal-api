#!/bin/sh

set -e

python manage.py migrate
python manage.py setup
gunicorn --bind :8080 --workers 5 wsgi 
