FROM python:3

# set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

WORKDIR /

RUN python3 -m venv /opt/venv

# # Install dependencies:
RUN pip install --upgrade pip
COPY python/requirements.txt .
RUN . /opt/venv/bin/activate
RUN pip install -r requirements.txt
# RUN pip install -r requirements.txt

ENV NLTK_DATA /usr/share/nltk_data

RUN pip install -U nltk
RUN pip install -U numpy
RUN python -m nltk.downloader -d /usr/share/nltk_data all

# # Run the application:
COPY python/flask_init.py .
COPY python/nltk_analysis.py .
COPY python/machine_learning.py .
COPY python/ .
COPY python/bin .
COPY python/wsgi.py .
# COPY python/bin/run.sh .
COPY gunicorn.conf.py .
EXPOSE 5000

# COPY . /
# WORKDIR /
# RUN pip install -r /requirements.txt

# ENTRYPOINT . /opt/venv/bin/activate && ["bash", "/bin/run.sh"]
CMD . /opt/venv/bin/activate && gunicorn --config ./gunicorn.conf.py --bind 0.0.0.0:5000 --timeout 120 --worker-class gevent --log-level debug wsgi:app

# this one 'works'=>
# ENTRYPOINT ["bash", "/bin/run.sh"]


# ENTRYPOINT [ "bash", "/app/bin/run.sh" ]
# CMD . /opt/venv/bin/activate
# CMD . /opt/venv/bin/activate && ["gunicorn --bind 0.0.0.0:5000 --worker-class gevent  wsgi:app"]
#CMD . /opt/venv/bin/activate && ["gunicorn", "--bind 0.0.0.0:5000", "--worker-class", "gevent", "wsgi:app"]
#CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--worker-class", "gevent", "--chdir", "/python/", "wsgi:app", "--reload"]
# CMD ["gunicorn --bind 0.0.0.0:5000 --worker-class gevent  wsgi:app"]

