from flask import Flask

from backend.config import app_config
from flask_pymongo import PyMongo
from flask_restful import Api
from backend.api.users import Users

mongo = PyMongo()


def create_app(env_name):
    """
    Create app
    """

    # app initiliazation
    app = Flask(__name__)

    app.config.from_object(app_config[env_name])
    mongo.init_app(app)

    api =Api(app)
    api.add_resource(Users, '/users')

    @app.route('/', methods=['GET'])
    def index():
        """
        example endpoint
        """
        return 'Congratulations! Your first endpoint is workin'

    return app