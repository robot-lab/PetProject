import json

from bson import json_util
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt_identity, get_raw_jwt,
                                jwt_refresh_token_required, jwt_required)
from flask_restful import Resource, reqparse

from backend.api.base_resource import BaseResource, UserBaseResource
import re

class Users(BaseResource):
    @jwt_required
    def get(self):
        clear_args = self.clear_args(self.parser.parse_args())
        res = self.mongo.db.users.find(clear_args)
        return json.loads(json.dumps([i for i in res], sort_keys=True, indent=4, default=json_util.default))


class UserRegistration(UserBaseResource):
    def post(self):
        data = self.parser.parse_args()

        user = self.mongo.db.users.find_one({'username': data['username']})
        if user:
            return {'message': f'User {data["username"]} already exists'}, 403
        if not re.search(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', data['email']):
            return {'message': f'Invalid email address {data["email"]}'}, 400
        try:
            data['password'] = self.generate_hash(data['password'])
            self.mongo.db.users.insert_one(data)
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': f'User {data["username"]} was created',
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 201
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogin(UserBaseResource):
    def post(self):
        data = self.parser.parse_args()
        current_user = self.mongo.db.users.find_one(
            {'username': data['username']})
        if not current_user:
            return {'message': f'User {data["username"]} doesn\'t exist'}
        if self.verify_hash(data['password'], current_user['password']):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': f'Logged in as {current_user["username"]}',
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            return {'message': 'Wrong credentials'}


class UserLogoutAccess(Resource):
    def post(self):
        return {'message': 'User logout'}


class UserLogoutRefresh(Resource):
    def post(self):
        return {'message': 'User logout'}


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}


class AllUsers(Resource):
    def get(self):
        return {'message': 'List of users'}

    def delete(self):
        return {'message': 'Delete all users'}
