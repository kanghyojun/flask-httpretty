from urllib.request import urlopen

import flask_httpretty

@flask_httpretty.activate
def test_pretty_get(f_app):
    uri = 'http://test.com'
    flask_httpretty.register_app(f_app, uri)
    body = 'hello world'
    resp = urlopen(uri + '/deals/').read()
    assert body == resp.decode('utf-8')
