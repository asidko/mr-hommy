import json
import random
import urllib
from os import environ

import requests
import schedule
from time import sleep

from datetime import datetime
from model import Notification, Configuration, config_default

APP_NAME = 'app-time-notify'
CONFIG_API_URL = environ.get('CONFIG_API_URL') or 'http://localhost:8010'
SPEAKER_API_URL = environ.get('SPEAKER_API_URL') or 'http://localhost:8050'

print('Request configs')
config_request = requests.post(f'{CONFIG_API_URL}/config/init/{APP_NAME}', json=config_default)

print('Loading configs', config_request.json())
config: Configuration = json.loads(config_request.text)


def speak(text: str, lang: str):
    print(f"Speaking text: '{text}' on lang='{lang}'")
    url_params = urllib.parse.urlencode({'text': text, 'lang': lang})
    try:
        requests.get(f'{SPEAKER_API_URL}/say?{url_params}')
    except IOError:
        print('Error sending speaking request.')


def say_notification_job(notification: Notification):
    print("Executing notification at time: " + notification['time'])
    text_to_say = random.choice(notification['texts'])
    lang = notification['lang']

    speak(text_to_say, lang)


if __name__ == '__main__':
    # Init schedules
    for notification in config['notifications']:
        print("Planing schedule at: %s" % notification['time'])
        try:
          time = datetime.strptime(notification['time'], '%H:%M');
          schedule.every().day.at(time.strftime('%H:%M')).do(say_notification_job, notification)
        except Exception as e:
           print("Error scheduling for time: {}. Details: {}".format(notification['time'], e))    

    # Start
    print("Run schedules...")
    while True:
        schedule.run_pending()
        sleep(1)
