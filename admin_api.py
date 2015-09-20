'''
Make the admin api
to add data about the shops and the data about services offered

POST actions both

Shop.info = name, id, address, phone, email
Shop.services : id , services:{'servicemae': unique id }

With the data added in the db, complete the get actions for client api

'''

from flask import Flask, jsonify, abort, make_response, url_for
from flask import request
from functools import wraps
from flask import request, Response
from api_authenticate import APIAutheticate
from shop import Shop

import json
import ConfigParser


class AdminApi:
    def __init__(self, config):
        self.app = Flask(__name__)
        self.api_authenticator = APIAutheticate(dict(config.items(
            "ADMIN_ENGINE")))
        self.api_port = config.getint("ADMIN_ENGINE", 'port')
        self.api_host = config.get("ADMIN_ENGINE", 'host')
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

        @self.app.route('/v1/shop/<string:shop_id>', methods=['POST'])
        @requires_auth
        def insert_shop(shop_id):
            print 'Shop id ', shop_id
            shop_details = request.data
            if len(shop_details) == 0:
                return make_response(
                    jsonify({'message': 'No shop info provided'}), 400)
            try:
                shop_info = json.loads(shop_details)
                print shop_info
                self.shop.insert_shop(shop_info)
            except Exception as e:
                print e
                return make_response(
                    jsonify({'message': 'shop info cannot be decoded'}), 400)
            print 'Here'
            ret = {'Message': 'OK'}
            return jsonify(ret)

        @self.app.route('/v1/services/shop/<string:shop_id>', methods=['POST'])
        @requires_auth
        def insert_services(shop_id):
            print 'Shop id ', shop_id
            services_data = request.data
            if len(services_data) == 0:
                return make_response(
                    jsonify({'message': 'No Service details provided'}), 400)
            try:
                services_list = json.loads(services_data)
                print services_list
                self.shop.insert_services(shop_id, services_list)
            except Exception as e:
                print e
                return make_response(
                    jsonify({'message': 'Service info cannot be decoded'}),
                    400)
            ret = {'Message': 'OK'}
            return jsonify(ret)

        self.app.run(host=self.api_host, port=self.api_port)

    @staticmethod
    def unauthorized():
        return make_response(jsonify({'error': 'Unauthorized access'}), 401)
