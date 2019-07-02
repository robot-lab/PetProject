from flask import Flask
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
from flask_restful import Api

from backend.api.events import Events
from backend.api.users import (TokenRefresh, UserSignin, UserSignoutAccess,
                               UserSignoutRefresh, UserRegistration, Users)
from backend.config import app_config

jwt = JWTManager()
mongo = PyMongo()


def create_app(env_name):
    app = Flask(__name__)

    app.config.from_object(app_config[env_name])
    mongo.init_app(app, uri=app.config['MONGO_URI'])
    jwt.init_app(app)

    api = Api(app)
    api.add_resource(Users, '/api/users')
    api.add_resource(Events, '/api/events')
    api.add_resource(UserRegistration, '/api/signup')
    api.add_resource(UserSignin, '/api/signin')
    api.add_resource(UserSignoutAccess, '/api/signout/access')
    api.add_resource(UserSignoutRefresh, '/api/signout/refresh')
    api.add_resource(TokenRefresh, '/api/token/refresh')

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization')
        response.headers.add(
            'Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return response
    
    def is_jti_blacklisted(jti):
        query = mongo.db.rt.find_one({"jti": jti})
        return bool(query)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return is_jti_blacklisted(jti)
    return app
