# gunicorn wsgi:app --bind 0.0.0.0:5000 --log-level=debug --workers=4

# source ../opt/venv/bin/activate
gunicorn --bind 0.0.0.0:5000 --worker-class gevent wsgi:app --workers=4 --reload
 