export DJANGO_SETTINGS_MODULE=settings.staging
python manage.py migrate
python manage.py runserver 8003