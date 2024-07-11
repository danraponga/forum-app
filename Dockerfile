FROM python:3.11-slim-buster

ENV PYTHONUNBUFFERED=1

WORKDIR /forum_app

COPY . /forum_app

RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev
