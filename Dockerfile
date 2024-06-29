FROM python:3.11-slim-buster

WORKDIR /forum_app

COPY . /forum_app

RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry lock \
    && poetry install --no-dev
