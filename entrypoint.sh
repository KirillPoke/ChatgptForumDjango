#!/bin/bash
sleep infinity
python "${VIRTUAL_ENV}"/bin/daphne -b 0.0.0.0 -p 80 django_server.asgi:application