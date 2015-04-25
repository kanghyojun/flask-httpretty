from flask import Flask

from urllib.request import urlopen, Request
from urllib.parse import urlencode

import flask_httpretty


HOST1 = 'http://test.com'
HOST2 = 'http://test2.com'
app2 = Flask(__name__)


@app2.route('/abc/', methods=['GET'])
def abc():
    return 'abc'


def uri(host, path):
    if not path.endswith('/'):
        path += '/'
    return '{}{}'.format(host, path)


def test_app_more_than_one(f_app):
    flask_httpretty.reset()
    flask_httpretty.register_app(f_app, HOST1)
    flask_httpretty.register_app(app2, HOST2)
    flask_httpretty.enable()
    body = 'hello world'
    resp = urlopen(uri(HOST1, '/deals/')).read()
    assert body == resp.decode('utf-8')
    resp = urlopen(uri(HOST2, '/abc/')).read()
    assert 'abc' == resp.decode('utf-8')
