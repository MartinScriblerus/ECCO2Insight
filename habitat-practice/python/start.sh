#!/bin/sh
. /opt/venv/bin/activate
gunicorn --bind 0.0.0.0:5000 --worker-class gevent wsgi:app