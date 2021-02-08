#!/bin/sh

set -e

python manage.py migrate
python manage setup
gunicorn --bind :8080 --workers 5 wsgi 
