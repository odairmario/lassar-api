#!/bin/bash

cd /home/app/lassar-api
echo ${CELERY_WORKER}
if [[ -v CELERY_WORKER  ]]; then
    celery -A lassarAPI worker -l info
else
    python3 manage.py wait_for_db
    python3 manage.py makemigrations record core
    python3 manage.py migrate
    daphne -b 0.0.0.0 -p 8000 lassarAPI.asgi:application
    
fi
