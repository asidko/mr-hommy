FROM python:3.8.7-slim-buster

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONIOENCODING utf-8

RUN apt-get update && apt-get install -y gcc libasound-dev portaudio19-dev python3-pyaudio
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "./main.py" ]

EXPOSE 8080