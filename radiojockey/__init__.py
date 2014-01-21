from flask import Flask, render_template, redirect
from flask.ext.cache import Cache
import requests
import io
import ConfigParser

def get_bbc_one():
    pls = requests.get('http://www.bbc.co.uk/radio/listen/live/r1_aaclca.pls')
    parser = ConfigParser.SafeConfigParser()
    parser.readfp(io.BytesIO(pls.content))
    url = parser.get('playlist', 'File1')
    return url

radiostations = {
    'bbc_one': {
        'name': 'BBC Radio 1',
        'function': get_bbc_one
    }
}

def mk_app(config):
    app = Flask('radiojockey')
    app.config.update(config)

    @app.route('/')
    def index():
        return render_template('index.htm', stations=radiostations)

    @app.route('/station/<sid>')
    def station(sid):
        url = radiostations[sid]['function']()
        return redirect(url, code=302)

    return app
