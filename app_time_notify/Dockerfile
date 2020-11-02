FROM python:3.8.6-alpine3.12

WORKDIR /app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED 1
COPY . .

CMD [ "python", "./main.py" ]

EXPOSE 8080