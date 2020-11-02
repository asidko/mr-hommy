import json
import random
import urllib
from os import environ

import requests
import schedule
import time

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
    url_params = urllib.parse.urlencode({text: text, lang: lang})
    try:
        requests.post(f'{SPEAKER_API_URL}?{url_params}')
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
        print("Plan schedule at: %s" % notification['time'])
        schedule.every().day.at(notification['time']).do(say_notification_job, notification)

    # Start
    print("Run schedules...")
    while True:
        schedule.run_pending()
        time.sleep(1)
