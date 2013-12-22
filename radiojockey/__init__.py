from flask import Flask, render_template, redirect
from flask.ext.cache import Cache
import requests
import io
import ConfigParser

cache = Cache()

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

@cache.memoize(3600)
def url_for_radiostation(sid):
    return radiostations[sid]['function']()

def mk_app(config):
    app = Flask('radiojockey')
    app.config.update(config)
    cache.init_app(app)

    @app.route('/')
    def index():
        return render_template('index.htm', stations=radiostations)

    @app.route('/station/<sid>')
    def station(sid):
        return redirect(url_for_radiostation(sid), code=302)

    return app
