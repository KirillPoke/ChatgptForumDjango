#!/bin/bash
python manage.py migrate
daphne -b localhost -p 80 -v 0 django_server.asgi:application & python manage.py qcluster