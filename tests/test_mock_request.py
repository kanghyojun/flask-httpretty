import json

from urllib.request import urlopen, Request
from urllib.parse import urlencode

import flask_httpretty
import pytest


HOST = 'http://test.com'

@pytest.fixture
def f_monkeypatch(f_app):
    flask_httpretty.register_app(f_app, HOST)
    flask_httpretty.enable()


def uri(path):
    if not path.endswith('/'):
        path += '/'
    return '{}{}'.format(HOST, path)


def test_pretty_get(f_monkeypatch):
    body = 'hello world'
    resp = urlopen(uri('/deals/')).read()
    assert body == resp.decode('utf-8')


def test_pretty_post(f_monkeypatch):
    body = {'name': 'myname', 'loc': 'seoul'}
    payload = urlencode(body).encode('utf-8')
    req = Request(uri('/create/'), payload, method='POST')
    resp = urlopen(req).read()
    assert body == json.loads(resp.decode('utf-8'))


def test_pretty_post_by_json(f_monkeypatch):
    body = {'name': 'myname', 'loc': 'seoul'}
    payload = json.dumps(body).encode('utf-8')
    req = Request(uri('/create/'), payload, method='POST',
                  headers={'Content-Type': 'application/json'})
    resp = urlopen(req).read()
    assert body == json.loads(resp.decode('utf-8'))


def test_pretty_put(f_monkeypatch):
    body = {'name': 'myname', 'loc': 'seoul'}
    payload = urlencode(body).encode('utf-8')
    req = Request(uri('/modify/'), payload, method='PUT')
    resp = urlopen(req).read()
    assert '{}' == resp.decode('utf-8')


def test_pretty_delete(f_monkeypatch):
    req = Request(uri('/delete/'), method='DELETE')
    resp = urlopen(req).read()
    assert '{}' == resp.decode('utf-8')


def test_pretty_get_with_query(f_monkeypatch):
    query = 'query'
    resp = urlopen(uri('/querystring/') + '?q={}'.format(query)).read()
    assert query == resp.decode('utf-8')
