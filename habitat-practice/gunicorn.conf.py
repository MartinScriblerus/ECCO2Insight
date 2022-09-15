import os
from socket import timeout

bind = "0.0.0.0:5000"
# workers = os.getenv('GUNICORN_WORKER_NUM', 1)
# workers = 4
worker_class = 'gevent'

timeout = 120
db_name = os.getenv('DB_NAME', 1)

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 1),
        'DB_NAME': os.getenv('DB_NAME', 1),
        'DB_USER': os.getenv('DB_USER', 1),
        'DB_PASSWORD': os.getenv('DB_PASSWORD', 1),
        'DB_HOST': os.getenv('DB_HOST', 1),
        'DB_PORT': os.getenv('DB_PORT', 1)
    }
}
import os
class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql+psycopg2://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join('./python', 'static/')