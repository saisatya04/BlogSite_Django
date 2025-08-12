#!/bin/bash
poetry run python manage.py collectstatic --no-input
poetry run python manage.py migrate

if [[ "$ENV_STATE" == "production" ]]; then
    poetry run gunicorn djangocourse.wsgi --workers 2 --forwarded-allow-ips "*"
else
    poetry run python manage.py runserver 0.0.0.0:8000
fi