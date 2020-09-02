from flask import Flask 
from flask import request
import os
import sys
from urllib.request import quote 
from os import environ

# Fix for Windows to find VLC folder
if sys.platform.startswith('win'):
	os.environ['PYTHON_VLC_MODULE_PATH'] = """C:\Program Files\VideoLan"""
	os.environ['PYTHON_VLC_LIB_PATH'] = """C:\Program Files\VideoLan\VLC\libvlc.dll"""
	import vlc
	vlc.Instance()
else:
	import vlc


app = Flask(__name__) 

RHVOICE_API_URL = environ.get('RHVOICE_API_URL') or 'http://localhost:8000'

###################################
# REST endpoints
###################################

@app.route('/say')
@app.route('/') 
def say_as_get_param():
	text = request.args.get('text') or "привет"
	play(text)
	return text

@app.route('/text/<the_text>')
def say_as_path_variable(the_text):
	text = the_text or "привет"
	play(text)
	return text

###################################
# Functions
###################################

def play(text):
	text = quote(text)
	url = RHVOICE_API_URL + "/say?text=" + text

	player = vlc.MediaPlayer(url)
	player.play()
	
if __name__ == '__main__': 
	app.run(host='0.0.0.0') 
