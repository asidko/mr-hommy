import json
from os import environ

import requests

APP_NAME = 'app-time-notify'
CONFIG_API_URL = environ.get('CONFIG_API_URL') or 'http://localhost:8010'

config_default = {
    'tasks': [
        {
            'cron': '00 6 * * *',
            'texts': ['Доброе утро. Уже 6 часов утра', '6 часов утра. Просыпайтесь.']
        }
    ]
}
config_request = requests.post(f'{CONFIG_API_URL}/config/init/{APP_NAME}', json=config_default)
config = json.loads(config_request.text)
