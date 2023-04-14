FROM python:slim-buster
WORKDIR /usr/src/app
RUN pip3 install python-telegram-bot
COPY . .
