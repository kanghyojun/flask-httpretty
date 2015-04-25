import functools

import httpretty.core as core

from httpretty.core import httpretty, URIInfo, fakesock, Entry
from httpretty.compat import ClassTypes, urlsplit
from httpretty.http import parse_requestline
from httpretty.utils import decode_utf8, utf8


old_fakesocket_sendall = fakesock.socket.sendall


def f_sendall(self, data, *args, **kw):
    self._sent_data.append(data)

    try:
        requestline, _ = data.split(b'\r\n', 1)
        method, path, version = parse_requestline(decode_utf8(requestline))
        is_parsing_headers = True
    except ValueError:
        is_parsing_headers = False

        if not self._entry:
            # If the previous request wasn't mocked, don't mock the subsequent sending of data
            return self.real_sendall(data, *args, **kw)
    self.fd.seek(0)

    if not is_parsing_headers:
        if len(self._sent_data) > 1:
            headers = utf8(last_requestline(self._sent_data))
            meta = self._entry.request.headers
            body = utf8(self._sent_data[-1])
            if meta.get('transfer-encoding', '') == 'chunked':
                if not body.isdigit() and body != b'\r\n' and body != b'0\r\n\r\n':
                    self._entry.request.body += body
            else:
                self._entry.request.body += body

            httpretty.historify_request(headers, body, False)
            return

    # path might come with
    s = urlsplit(path)
    core.POTENTIAL_HTTP_PORTS.add(int(s.port or 80))
    headers, body = list(map(utf8, data.split(b'\r\n\r\n', 1)))

    request = flaskhttpretty.historify_request(headers, body)

    info = URIInfo(hostname=self._host, port=self._port,
                   path=s.path,
                   query=s.query,
                   last_request=request)
    entry = flaskhttpretty.get_entry(method, info, request)
    if not entry:
        self._entry = None
        self.real_sendall(data)
        return None

    self._entry = entry


class flaskhttpretty(httpretty):

    flask_app = None

    _apps = []

    @classmethod
    def check_response(cls, responses, method, info, request):
        result_response = None
        for response in responses:
            if response.status_code != 404:
                 result_response = response

        return cls.flask_resp_to_entry(result_response, method, info, request)


    @classmethod
    def get_entry(cls, method, info, request):
        if not cls._apps:
            return None
        responses = []
        for app in cls._apps:
            with app.test_client() as c:
                http_request = getattr(c, method.lower())
                content_type = request.headers.get('Content-Type')
                response = http_request('{}?{}'.format(info.path, info.query),
                                        data=request.body,
                                        content_type=content_type)
                responses.append(response)

        return cls.check_response(responses, method, info, request)


    @classmethod
    def register_app(cls, app, uri='http://localhost:9000'):
        cls.uri = uri
        cls._apps.append(app)

    @classmethod
    def enable(cls):
        fakesock.socket.sendall = f_sendall
        httpretty.enable()

    @classmethod
    def reset(cls):
        cls._apps = []
        httpretty.reset()

    @classmethod
    def flask_resp_to_entry(cls, resp, method, info, request):
        headers = {}
        headers['Content-Type'] = resp.content_type
        return Entry(method, info.hostname, body=resp.data,
                     status=resp.status_code,
                     adding_headers=None, forcing_headers=None)


def flaskhttprettified(test):
    "A decorator tests that use HTTPretty"
    def decorate_class(klass):
        for attr in dir(klass):
            if not attr.startswith('test_'):
                continue

            attr_value = getattr(klass, attr)
            if not hasattr(attr_value, "__call__"):
                continue

            setattr(klass, attr, decorate_callable(attr_value))
        return klass

    def decorate_callable(test):
        @functools.wraps(test)
        def wrapper(*args, **kw):
            flaskhttpretty.reset()
            flaskhttpretty.enable()
            try:
                return test(*args, **kw)
            finally:
                flaskhttpretty.disable()
        return wrapper

    if isinstance(test, ClassTypes):
        return decorate_class(test)
    return decorate_callable(test)
