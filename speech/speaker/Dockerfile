FROM python:3.8.6-slim-buster

RUN apt-get update \ 
	&& apt-get install -y vlc-bin vlc-data vlc-plugin-base
WORKDIR /app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED 1
COPY . .

CMD [ "python", "./main.py" ]

EXPOSE 8080
