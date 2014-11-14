from flask import Flask
from pytest import fixture

@fixture
def f_app():
    app =  Flask(__name__)
    @app.route('/deals/', methods=['GET'])
    def deals():
        return 'hello world'

    return app
