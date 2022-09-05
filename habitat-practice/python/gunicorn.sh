#!bin/sh
set -e
gunicorn --bind 0.0.0.0:5000 --worker-class gevent  wsgi:app