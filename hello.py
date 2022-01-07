from flask import Flask
from flask_cors import CORS
from logging.config import dictConfig
import requests


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi']
    }
})


app = Flask(__name__)
cors = CORS(app)

mystrom_switch_base_url = 'http://192.168.0.50/'

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/switch-status')
def status():
    response_content = requests.get(mystrom_switch_base_url + 'report').content
    print('status: {}'.format(response_content))
    return response_content

@app.route('/switch-on')
def switch_on():
    return requests.get(mystrom_switch_base_url + 'relay?state=1').content

@app.route('/switch-off')
def switch_off():
    return requests.get(mystrom_switch_base_url + 'relay?state=0').content

@app.route('/switch-toggle')
def switch_toggle():
    response_content = requests.get(mystrom_switch_base_url + 'toggle').content
    print('switch-toggle: {}'.format(response_content))
    return response_content
