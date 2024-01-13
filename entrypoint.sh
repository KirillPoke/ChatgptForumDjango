#!/bin/bash
python manage.py makemigrations
daphne -b 0.0.0.0 -p 443 django_server.asgi:application