import json

from urllib.request import urlopen, Request
from urllib.parse import urlencode

import flask_httpretty

@flask_httpretty.activate
def test_pretty_get(f_app):
    uri = 'http://test.com'
    flask_httpretty.register_app(f_app, uri)
    body = 'hello world'
    resp = urlopen(uri + '/deals/').read()
    assert body == resp.decode('utf-8')


@flask_httpretty.activate
def test_pretty_post(f_app):
    uri = 'http://test.com'
    flask_httpretty.register_app(f_app, uri)
    body = {'name': 'myname', 'loc': 'seoul'}
    payload = urlencode(body).encode('utf-8')
    req = Request(uri + '/create/', payload, method='POST')
    resp = urlopen(req).read()
    assert body == json.loads(resp.decode('utf-8'))


@flask_httpretty.activate
def test_pretty_post_by_json(f_app):
    uri = 'http://test.com'
    flask_httpretty.register_app(f_app, uri)
    body = {'name': 'myname', 'loc': 'seoul'}
    payload = json.dumps(body).encode('utf-8')
    req = Request(uri + '/create/', payload, method='POST',
                  headers={'Content-Type': 'application/json'})
    resp = urlopen(req).read()
    assert body == json.loads(resp.decode('utf-8'))


@flask_httpretty.activate
def test_pretty_put(f_app):
    uri = 'http://test.com'
    flask_httpretty.register_app(f_app, uri)
    body = {'name': 'myname', 'loc': 'seoul'}
    payload = urlencode(body).encode('utf-8')
    req = Request(uri + '/modify/', payload, method='PUT')
    resp = urlopen(req).read()
    assert '{}' == resp.decode('utf-8')


@flask_httpretty.activate
def test_pretty_delete(f_app):
    uri = 'http://test.com'
    flask_httpretty.register_app(f_app, uri)
    req = Request(uri + '/delete/', method='DELETE')
    resp = urlopen(req).read()
    assert '{}' == resp.decode('utf-8')
