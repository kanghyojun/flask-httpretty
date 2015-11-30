Flask-httpretty
=================

.. image:: https://travis-ci.org/admire93/flask-httpretty.svg?branch=master
   :target: https://travis-ci.org/admire93/flask-httpretty

Mock http request with flask!

flask-httpretty is built based on httpretty_.


Hello world
~~~~~~~~~~~~

.. code-block:: python

   from flask import Flask
   from urllib.request import urlopen

   import flask_httpretty


   app = Flask(__name__)


   @app.route('/', methods=['GET'])
   def hello_world():
       return 'hello world'


   @flask_httpretty.activate
   def test_hello_world():
       flask_httpretty.register_app(app, 'http://hellotest.com')
       resp = urlopen('http://hellotest.com').read()
       assert 'hello world' == resp.decode('utf-8')


Officially supported libraries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Since flask-httpretty use httpretty_ to monkey patches pythons'socket,
it support same libraries `httpretty do`_. these are

* requests_
* httplib2_
* urllib_

.. _httpretty: https://github.com/gabrielfalcao/HTTPretty
.. _requests: http://docs.python-requests.org/en/latest/
.. _httplib2: http://code.google.com/p/httplib2/
.. _urllib: https://docs.python.org/3.4/library/urllib.request.html
.. _`httpretty do`: https://github.com/gabrielfalcao/HTTPretty#officially-supported-libraries
