#!/bin/bash

if [ "$SERVICE_TYPE" = "django" ]; then
    echo "Initializing Django container..."
	python manage.py makemigrations
    python manage.py migrate
    python manage.py collectstatic --noinput
    python manage.py runserver 0.0.0.0:8000
elif [ "$SERVICE_TYPE" = "celery" ]; then
    echo "Initializing Celery container..."
    celery --app=testproj worker -l INFO
fi
