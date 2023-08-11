#! /usr/bin/bash

source ../venv/bin/activate
gnome-terminal -- sh -c 'celery -A ozon_parser worker'
gnome-terminal -- sh -c 'python manage.py runserver'
sleep 2
curl 'http://127.0.0.1:8000/bot/'