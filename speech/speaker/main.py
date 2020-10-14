import os

import sys
from flask import Flask
from flask import request
from os import environ
from urllib.request import quote
import requests
import json

# Fix for Windows to find VLC folder
from model import Configuration, config_default

if sys.platform.startswith('win'):
    os.environ['PYTHON_VLC_MODULE_PATH'] = """C:\Program Files\VideoLan"""
    os.environ['PYTHON_VLC_LIB_PATH'] = """C:\Program Files\VideoLan\VLC\libvlc.dll"""
    import vlc

    vlc.Instance()
else:
    import vlc

APP_NAME = 'speaker'
RHVOICE_API_URL = environ.get('RHVOICE_API_URL') or 'http://localhost:8000'
CONFIG_API_URL = environ.get('CONFIG_API_URL') or 'http://localhost:8010'

config_request = requests.post(f'{CONFIG_API_URL}/config/init/{APP_NAME}', json=config_default)
config: Configuration = json.loads(config_request.text)

app = Flask(APP_NAME)


@app.route('/say')
@app.route('/')
def say_as_get_param():
    text = request.args.get('text') or ''
    if not text:
        return 'No text given. Pass parameters like ?text=Hello&voice=en'

    lang = request.args.get('lang') or 'ru'
    voice = request.args.get('voice') \
            or config['voices'][lang] \
            or config['default_voice_name']

    play(text, voice)

    return text


def play(text, voice):
    text = quote(text)
    url = RHVOICE_API_URL + "/say?text=" + text
    url = url + "&voice=" + voice if voice is not None else url

    print(f'Playing url: {url}')
    player = vlc.MediaPlayer(url)
    player.play()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
