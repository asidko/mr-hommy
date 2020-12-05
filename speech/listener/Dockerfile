FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 -y
RUN apt-get install  -y python3.8 python3.8-dev python3-pip flac sox python-pyaudio python3-pyaudio
RUN pip3 install Speechrecognition && pip3 install --allow-external pyaudio --allow-unverified pyaudio pyaudio


WORKDIR /app


ENV PYTHONUNBUFFERED 1
ENV PYTHONIOENCODING utf-8
COPY . .

CMD [ "python3", "./main.py" ]

EXPOSE 8080
