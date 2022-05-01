FROM python:3.9.1-slim-buster
WORKDIR /usr/src/app

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV REDIS_URL=redis://redis:6379/0
ENV MONGO_URL=mongodb://mongo:27017/app_development

#Server will reload itself on file changes if in dev mode

ENV FLASK_ENV=development 
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .
