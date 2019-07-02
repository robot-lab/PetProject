from flask_restful import Resource, reqparse
from backend.api.base_resource import BaseResource
import json
from bson import json_util


class Events(BaseResource):
    def __init__(self):
        super(Events, self).__init__()
        self.parser.add_argument('title', type=str)
        self.parser.add_argument('type', type=str)
        self.parser.add_argument('date', type=str)
        self.parser.add_argument('id', type=int)
        self.parser.add_argument('city', type=str)
    
    def get(self):
        clear_args = self.clear_args(self.parser.parse_args())
        res = self.mongo.db.events.find(clear_args)
        return json.loads(json.dumps([i for i in res], sort_keys=True, indent=4, default=json_util.default))

    def post(self):
        try: 
            clear_args = self.clear_args(self.parser.parse_args())
            if clear_args:
                self.mongo.db.events.insert_one(clear_args)
            else:
                return json.dumps({'message' : 'NAH'})
            return json.dumps({'message' : 'SUCCESS'})
        except Exception:
            return json.dumps({'error' : str(Exception)})

