# syntax=docker/dockerfile:1
FROM python:3.11-slim

ARG DEBIAN_FRONTEND=noninteractive


RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10 && \
  echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' > /etc/apt/sources.list.d/mongodb.list && \
  apt-get update \
  && apt-get install -y --no-install-recommends \
  git build-essential cmake libssl-dev pkg-config curl mongodb-org \
  && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip setuptools wheel && pip install --no-cache-dir fastapi "uvicorn[standard]" websockets && pip install -U -q transformers torch 

VOLUME [ "/app/db" ]

WORKDIR /app

COPY server.py /app/server/server.py

EXPOSE 8000


CMD ["mongod","uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 27017
EXPOSE 28017
