#!/bin/bash
python manage.py migrate
daphne -b 0.0.0.0 -p 80 -v 0 django_server.asgi:application & python manage.py qcluster