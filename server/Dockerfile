# FROM python:3.9.1-slim-buster
# FROM luyangliuable/fit3170_alpine_image:6.3
FROM alpine:3.14

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app/server/

RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

RUN pip install pip==22.2.2

RUN pip install --upgrade pip \
    && pip install --no-cache-dir \
        awscli \
    && rm -rf /var/cache/apk/*

RUN aws --version   # Just to make sure its installed alright

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
# ENV REDIS_URL=redis://redis:6379/0
# ENV MONGO_URL=mongodb://username:password@mongodb

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#Server will reload itself on file changes if in dev mode
ENV FLASK_ENV=development 

RUN pip3 install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# aws 
COPY .aws /root/.aws

# copy project
# COPY . .

RUN echo env