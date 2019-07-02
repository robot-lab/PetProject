from flask_restful import Resource, reqparse
from passlib.hash import pbkdf2_sha256 as sha256


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
        self.parser.add_argument('username', type=str, help = 'This field cannot be blank', required = True)
        self.parser.add_argument('password', type=str, help = 'This field cannot be blank', required = True)
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('email', type=str, help = 'This field cannot be blank', required = True)

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)
        
    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)
