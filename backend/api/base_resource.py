from flask_restful import Resource, reqparse
from passlib.hash import pbkdf2_sha256 as sha256
import re

class BaseResource(Resource):
    def __init__(self):
        super(BaseResource, self).__init__()   
        from backend import mongo
        self.mongo = mongo
        self.parser = reqparse.RequestParser()

    @staticmethod
    def clear_args(args):
        return {key: value for key, value in args.items() if value}


class UserBaseResource(BaseResource):
    def __init__(self):
        super(UserBaseResource, self).__init__()
        self.parser.add_argument('username', type=str)
        self.parser.add_argument('password', type=str)
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('email', type=str)

    @staticmethod
    def validate_user_data(data):
        if not data['email']:
            return {'message': f'No email provided'}, False
        if not data['username']:
            return {'message': f'No username provided'}, False
        if not data['password']:
            return {'message': f'No password provided'}, False
        if not re.search(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', data['email']):
            return {'message': f'Invalid email address {data["email"]}'}, False
        return {'message': 'Ok'}, True

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)
        
    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)   
