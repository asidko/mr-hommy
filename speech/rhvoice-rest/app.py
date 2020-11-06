import hashlib
import os
import re
import subprocess
import urllib
from flask import Flask, request, send_from_directory, after_this_request
from shlex import quote

app = Flask(__name__, static_url_path='')
data_path = "/opt/data"

DEFAULT_VOICE = os.environ.get('DEFAULT_VOICE') or 'aleksandr'

@app.route('/say')
def say():
    textArg = request.args.get('text') or 'привет'
    voiceArg = request.args.get('voice')

    text = re.sub('[\r\n]',' ', urllib.parse.unquote(textArg))

    m = hashlib.md5()
    m.update(text.encode('utf-8'))
    file_name = m.hexdigest()
    file_path = os.path.join(data_path, file_name)

    voice = "-p %s" % (DEFAULT_VOICE) if voiceArg is None else "-p %s" % (voiceArg)

    cmd = "echo %s | RHVoice-test %s -o %s.wav && lame %s.wav %s.mp3" % (quote(text), voice, file_path, file_path, file_path)
    subprocess.call([cmd], shell=True)

    @after_this_request
    def remove_file(response):
        os.remove("%s.wav" % (file_path))
        os.remove("%s.mp3" % (file_path))
        return response

    return send_from_directory(data_path, "%s.wav" % (file_name))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
