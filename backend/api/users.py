from flask_restful import Resource, reqparse
from backend.api.base_resource import BaseResource
import json
from bson import json_util


class Users(BaseResource):
    def get(self):
        print("HERE")
        self.parser.add_argument('username', type=str)
        self.parser.add_argument('age', type=int)
        args = self.parser.parse_args()
        clear_args = {key: value for key, value in args.items() if value}
        res = self.mongo.db.users.find(clear_args)
        return json.loads(json.dumps([i for i in res], sort_keys=True, indent=4, default=json_util.default))
    

