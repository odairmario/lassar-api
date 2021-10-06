#!/bin/bash

cd /home/app/bbbrecord_api
echo ${CELERY_WORKER}
if [[ -v CELERY_WORKER  ]]; then
    celery -A bbbrecord_api worker -l info
else
    python3 manage.py wait_for_db
    python3 manage.py makemigrations record core
    python3 manage.py migrate
    daphne -b 0.0.0.0 -p 8000 bbbrecord_api.asgi:application
    
fi
