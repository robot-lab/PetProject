from flask_restful import Resource


class Users(Resource):
    def get(self):
        from backend import mongo
        mongo.db.test.insert_one({'lol': 'lol'})
        test = mongo.db.test.find_one().drop('_id', None)
        return test
