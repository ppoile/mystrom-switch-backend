from flask import Flask
from flask_cors import CORS
import requests

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
