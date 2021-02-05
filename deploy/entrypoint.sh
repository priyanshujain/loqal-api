#!/bin/sh

set -e

python manage.py migrate

gunicorn --bind :8080 --workers 4 wsgi
