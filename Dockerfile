FROM alpine:3.14

ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools


RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python

WORKDIR /usr/src/app

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV REDIS_URL=redis://redis:6379/0
ENV MONGO_URL=mongodb://username:password@mongodb

#Server will reload itself on file changes if in dev mode

ENV FLASK_ENV=development 
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD python app.py