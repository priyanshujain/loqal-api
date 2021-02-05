#!/bin/sh

set -e

python manage.py migrate

gunicorn --bind :8000 --workers 4 wsgi
