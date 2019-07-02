import json

from bson import json_util
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt_identity, get_raw_jwt,
                                jwt_refresh_token_required, jwt_required)
from flask_restful import Resource, reqparse

from backend.api.base_resource import BaseResource, UserBaseResource


class Users(BaseResource):
    @jwt_required
    def get(self):
        clear_args = self.clear_args(self.parser.parse_args())
        res = self.mongo.db.users.find(clear_args)
        return json.loads(json.dumps([i for i in res], sort_keys=True, indent=4, default=json_util.default))


class UserRegistration(UserBaseResource):
    def post(self):
        data = self.parser.parse_args()
        msg, status = self.validate_user_data(data)
        if not status:
            return msg, 400
        
        user = self.mongo.db.users.find_one({'username': data['username']})
        if user:
            return {'message': f'User {data["username"]} already exists'}, 403
        
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


class UserSignin(UserBaseResource):
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


class UserSignoutAccess(BaseResource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            self.mongo.db.rt.insert_one({"jti": jti})
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class UserSignoutRefresh(BaseResource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            self.mongo.db.rt.insert_one({"jti": jti})
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}
