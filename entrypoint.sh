#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Running Django Migrations..."
python manage.py migrate --noinput

echo "Collecting Static Files..."
python manage.py collectstatic --noinput --clear

# echo "Creating superuser if it doesn't exist (non-interactive)"
# python manage.py shell << END_SCRIPT
# from django.contrib.auth import get_user_model
# User = get_user_model()
# if not User.objects.filter(username='${DJANGO_SUPERUSER_USERNAME:-admin}').exists():
#     User.objects.create_superuser('${DJANGO_SUPERUSER_USERNAME:-admin}', '${DJANGO_SUPERUSER_EMAIL:-admin@example.com}', '${DJANGO_SUPERUSER_PASSWORD:-adminpass}')
#     print('Superuser created.')
# else:
#     print('Superuser already exists.')
# END_SCRIPT
# The above superuser creation is better handled once, or via fixtures, or manually after initial setup.
# For automated setup, it might run on every container start if not careful.

# Start Gunicorn server
echo "Starting Gunicorn..."
exec gunicorn taf_project.wsgi:application --bind 0.0.0.0:8000 --workers 3 --log-level info
