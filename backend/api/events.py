import json

from bson import json_util
from flask_restful import Resource, reqparse

from backend.api.base_resource import EventBaseResource


class Events(EventBaseResource):
    def get(self):
        clear_args = self.clear_args(self.parser.parse_args())
        res = self.mongo.db.events.find(clear_args)
        return json.loads(json.dumps([i for i in res], sort_keys=True, indent=4, default=json_util.default)), 200

    def post(self):
        try:
            clear_args = self.clear_args(self.parser.parse_args())
            if clear_args:
                self.mongo.db.events.insert_one(clear_args)
            else:
                return {'message': 'Something went wrong'}, 500
            return {'message': 'Ok'}, 200
        except Exception:
            return json.dumps({'error': str(Exception)}), 500

    def delete(self):
        clear_args = self.clear_args(self.parser.parse_args())
        res = self.mongo.db.events.delete_one({'id': str(clear_args['id'])}) #I don't know which key we will be using
        print(res.acknowledged, res.deleted_count, res.raw_result)
        if res.deleted_count == 1:
            return {'message': 'Ok'}, 204
        else:
            return {'message': 'Document has not been found and deleted'}, 404

    def put(self):
        pass
