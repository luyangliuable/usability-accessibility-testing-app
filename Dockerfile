FROM python:3.9.1-slim-buster

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
# ENV REDIS_URL=redis://redis:6379/0
# ENV MONGO_URL=mongodb://username:password@mongodb

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#Server will reload itself on file changes if in dev mode
ENV FLASK_ENV=development 

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

RUN echo env