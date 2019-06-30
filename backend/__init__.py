from flask import Flask

from backend.config import app_config
from flask_pymongo import PyMongo
from flask_restful import Api
from backend.api.users import Users
from backend.api.events import Events

mongo = PyMongo()


def create_app(env_name):
    """
    Create app
    """

    # app initiliazation
    app = Flask(__name__)

    app.config.from_object(app_config[env_name])
    mongo.init_app(app, uri=app.config['MONGO_URI'])

    api = Api(app)
    api.add_resource(Users, '/users')
    api.add_resource(Events, '/events')

    return app