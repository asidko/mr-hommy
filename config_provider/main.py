from os import environ
import couchdb2
from flask import Flask, request

# Configuration #############################
DB_HOST = environ.get('DB_HOST') or 'localhost'
DB_USER = environ.get('DB_USER') or 'admin'
DB_PASSWORD = environ.get('DB_PASSWORD') or 'admin'
DB_URL = f"http://{DB_HOST}:5984/"

# Initialization ############################
app = Flask(__name__)

print('Connecting to: ' + DB_URL)
server = couchdb2.Server(DB_URL, DB_USER, DB_PASSWORD)

if 'app_configs' in server:
    db = server['app_configs']
else:
    db = server.create('app_configs')


@app.route('/config/init/<app_name>', methods=['POST'])
def create_app_configuration(app_name: str):
    new_app_config = request.get_json(force=True)

    config_doc = {
        '_id': app_name,
        'app_name': app_name,
        'config': new_app_config
    }
    db.update([config_doc])

    return config_doc['config']


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
