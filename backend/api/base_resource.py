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
    def validate_password(password):
        '''
        Verify the strength of password
        Returns a dict indicating the wrong criteria
        A password is considered strong if:
            8 characters length or more
            1 digit or more
            1 symbol or more
            1 uppercase letter or more
            1 lowercase letter or more
       '''
        # calculating the length
        length_error = len(password) < 8

        # searching for digits
        digit_error = re.search(r"\d", password) is None

        # searching for uppercase
        uppercase_error = re.search(r"[A-Z]", password) is None

        # searching for lowercase
        lowercase_error = re.search(r"[a-z]", password) is None

        # overall result
        password_ok = not (
            length_error or digit_error or uppercase_error or lowercase_error)

        return {
            'password_ok': password_ok,
            'length_error': length_error,
            'digit_error': digit_error,
            'uppercase_error': uppercase_error,
            'lowercase_error': lowercase_error,
            }


    @staticmethod
    def validate_user_data(data):
        if not data['email']:
            return {'message': f'No email provided'}, False
        if not re.search(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', data['email']):
            return {'message': f'Invalid email address {data["email"]}'}, False
        if not data['username']:
            return {'message': f'No username provided'}, False
        if not data['password']:
            return {'message': f'No password provided'}, False
        password_res = UserBaseResource.validate_password(data['password'])
        if not password_res['password_ok']:
            return {'message': f'{password_res}'}, False
       
        return {'message': 'Ok'}, True

    
    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)
