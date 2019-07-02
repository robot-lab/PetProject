from flask import Flask
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
from flask_restful import Api

from backend.api.events import Events
from backend.api.users import (TokenRefresh, UserLogin, UserLogoutAccess,
                               UserLogoutRefresh, UserRegistration, Users)
from backend.config import app_config

jwt = JWTManager()
mongo = PyMongo()


def create_app(env_name):
    """
    Create app
    """

    # app initiliazation
    app = Flask(__name__)

    app.config.from_object(app_config[env_name])
    mongo.init_app(app, uri=app.config['MONGO_URI'])
    jwt.init_app(app)

    api = Api(app)
    api.add_resource(Users, '/users')
    api.add_resource(Events, '/events')
    api.add_resource(UserRegistration, '/registration')
    api.add_resource(UserLogin, '/login')
    api.add_resource(UserLogoutAccess, '/logout/access')
    api.add_resource(UserLogoutRefresh, '/logout/refresh')
    api.add_resource(TokenRefresh, '/token/refresh')

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization')
        response.headers.add(
            'Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return response

    return app
