from flask import Flask
from flask_cors import CORS
from logging.config import dictConfig
import requests
import threading


dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] [%(levelname)s] %(module)s: %(message)s',
        },
    },
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi'],
    }
})


MYSTROM_SWITCH_BASE_URL = 'http://192.168.0.32/'
AUTO_OFF_DELAY_IN_SECONDS = 15 * 60


app = Flask(__name__)
cors = CORS(app)


def timer_switch_off():
    app.logger.info('switch off (timer)')
    requests.get(MYSTROM_SWITCH_BASE_URL + 'relay?state=0')
auto_off_timer = threading.Timer(AUTO_OFF_DELAY_IN_SECONDS, timer_switch_off)


def start_auto_off_timer():
    global auto_off_timer
    app.logger.info('auto-off timer started...')
    auto_off_timer = threading.Timer(AUTO_OFF_DELAY_IN_SECONDS, timer_switch_off)
    auto_off_timer.start()


def cancel_auto_off_timer():
    app.logger.info('auto-off timer cancelled...')
    auto_off_timer.cancel()


@app.route('/')
def index():
    app.logger.info('index')
    return '''<h1>Index Page</h1>
<p><a href="/hello">Get hello message</a></p>
<p><a href="/switch-status">Get switch status</a></p>
<p><a href="/switch-on">Switch on (with auto-switch-off)</a></p>
<p><a href="/switch-off">Switch off</a></p>
<p><a href="/switch-toggle">Toggle switch (with auto-switch-off)</a></p>
'''

@app.route('/hello')
def hello():
    app.logger.info('hello')
    return 'Hello, world.'

@app.route('/switch-status')
def status():
    app.logger.debug('status...')
    response_content = requests.get(MYSTROM_SWITCH_BASE_URL + 'report').content
    app.logger.info('status: {}'.format(response_content))
    return response_content

@app.route('/switch-on')
def switch_on():
    app.logger.info('switch on')
    retval = requests.get(MYSTROM_SWITCH_BASE_URL + 'relay?state=1').content
    start_auto_off_timer()
    return retval

@app.route('/switch-off')
def switch_off():
    app.logger.info('switch off')
    cancel_auto_off_timer()
    return requests.get(MYSTROM_SWITCH_BASE_URL + 'relay?state=0').content

@app.route('/switch-toggle')
def switch_toggle():
    app.logger.debug('switch toggle...')
    response = requests.get(MYSTROM_SWITCH_BASE_URL + 'toggle')
    app.logger.info('switch-toggle: {}'.format(response.content))
    relay_on = response.json()['relay']
    if relay_on:
        start_auto_off_timer()
    else:
        cancel_auto_off_timer()
    return response.content
