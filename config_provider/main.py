from os import environ


RHVOICE_API_URL = environ.get('RHVOICE_API_URL') or 'http://localhost:8000'


###################################
# REST endpoints
###################################

@app.route('/config/init/<app_name>')
def say_as_path_variable(the_text):
  text = the_text or "привет"
  play(text, None)
  return text


###################################
# Functions
###################################

def play(text, voice):
  text = quote(text)
  url = RHVOICE_API_URL + "/say?text=" + text
  url = url + "&voice=" + voice if voice is not None else url

  print(f'Playing url: {url}')
  player = vlc.MediaPlayer(url)
  player.play()


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)
