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
server = couchdb2.Server(href=DB_URL, username=DB_USER, password=DB_PASSWORD,
                use_session=False, ca_file=None)

if 'app_configs' in server:
    db = server['app_configs']
else:
    db = server.create('app_configs')


@app.route('/config/init/<app_name>', methods=['POST'])
def create_app_configuration(app_name: str):
    print('Got init request from app: %s' % app_name)
    new_app_config = request.get_json(force=True)
    
    if app_name in db:
      return db[app_name]['config'] or {}
      
    config_doc = {
        '_id': app_name,
        'app_name': app_name,
        'config': new_app_config
    }
    
    print('Updating config:', config_doc)
    db.update([config_doc])

    return config_doc['config']


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
