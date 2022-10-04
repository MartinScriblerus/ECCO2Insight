### config.py ###
import os
# Scheme: "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"

# DATABASE_URI = 'postgresql+psycopg2://postgres:password@localhost:5432/matthewreilly'
DATABASE_URI = 'postgresql+psycopg2://postgres:postgres@db:5432/books'
DATABASE_URL = 'postgres:postgres@db:5432/matthewreilly'
API_KEY = '?wskey=orperesbula'
DB_ENGINE='postgresql+psycopg2://postgres:postgres@db:5432/books'
DB_USER='postgres'
DB_PASSWORD='postgres'
DB_NAME='books'
DB_PORT=5432
PORT_APP: 5000

DEBUG=1
SECRET_KEY='foo'
import os
class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql+psycopg2://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
