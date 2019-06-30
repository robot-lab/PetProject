from flask_restful import Resource
import json
from bson import json_util


class Users(Resource):
    def get(self):
        from backend import mongo
        mongo.db.test.insert_one({'lol': 'lol'})
        return json.loads(json.dumps([i for i in mongo.db.test.find()],
                                     sort_keys=True, indent=4, default=json_util.default))

