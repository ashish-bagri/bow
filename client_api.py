'''
API to get services available for a given shop

'''

from flask import Flask, jsonify, abort, make_response, url_for
from flask import request
from functools import wraps
from flask import request, Response
from api_authenticate import APIAutheticate
from shop import Shop


class ClientAPI:
    def __init__(self, config):
        self.app = Flask(__name__)
        self.api_authenticator = APIAutheticate(dict(config.items(
            "CLIENT_ENGINE")))
        self.api_port = config.getint("CLIENT_ENGINE", 'port')
        self.api_host = config.get("CLIENT_ENGINE", 'host')
        self.shop = Shop(config)

    def run(self):
        def requires_auth(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                if not self.api_authenticator.authenticate(request.headers):
                    return self.unauthorized()

                return f(*args, **kwargs)

            return decorated

        def shop_not_found():
            return make_response(jsonify({'message': 'Not found'}), 404)

        @self.app.route('/v1/services/shop/<string:shop_id>', methods=['GET'])
        @requires_auth
        def get_services(shop_id):
            try:
                print 'Shop id ', shop_id
                services_list = self.shop.get_services(shop_id)
                return jsonify(services_list)
            except Exception as e:
                print e

        self.app.run(host=self.api_host, port=self.api_port)

    @staticmethod
    def unauthorized():
        return make_response(jsonify({'error': 'Unauthorized access'}), 401)
