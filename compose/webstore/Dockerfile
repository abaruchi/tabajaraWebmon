FROM python:3.7

ENV PYTHONUNBUFFERED 1

COPY requirements/requirements-webstore.txt /requirements.txt

COPY compose/webstore/start.sh /start.sh
RUN chmod +x /start.sh

RUN pip install -r /requirements.txt

RUN apt-get update

WORKDIR /webstore

