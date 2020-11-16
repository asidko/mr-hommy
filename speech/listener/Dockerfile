FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 -y
RUN apt-get install python3.8 python3.8-dev python3-pip -y

WORKDIR /app

COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

ENV PYTHONUNBUFFERED 1
COPY . .

CMD [ "python3", "./main.py" ]

EXPOSE 8080
