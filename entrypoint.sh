#!/bin/bash
python manage.py check --deploy
daphne django_server.asgi:application