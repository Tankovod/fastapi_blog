FROM python:3.11.5-alpine3.18

WORKDIR /app

COPY . /app

#COPY ./requirements.txt /app/requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

EXPOSE 8001