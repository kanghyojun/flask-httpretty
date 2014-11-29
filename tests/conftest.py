from flask import Flask, request, jsonify, abort
from pytest import fixture

@fixture
def f_app():
    app =  Flask(__name__)
    @app.route('/querystring/', methods=['GET'])
    def querystring():
        return request.args.get('q', '')

    @app.route('/deals/', methods=['GET'])
    def deals():
        return 'hello world'

    @app.route('/create/', methods=['POST'])
    def create():
        if request.json:
            name = request.json.get('name')
            loc = request.json.get('loc')
        else:
            name = request.form.get('name')
            loc = request.form.get('loc')
        return jsonify(name=name, loc=loc), 201

    @app.route('/modify/', methods=['PUT'])
    def mod():
        name = request.form.get('name')
        loc = request.form.get('loc')
        if name is None or loc is None:
            abort(400)
        return jsonify()

    @app.route('/delete/', methods=['DELETE'])
    def dele():
        return jsonify()

    return app
