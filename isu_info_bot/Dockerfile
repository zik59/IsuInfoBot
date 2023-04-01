# syntax=docker/dockerfile:1
FROM python:3.8-alpine
WORKDIR /code

COPY requirements.txt /code
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /code