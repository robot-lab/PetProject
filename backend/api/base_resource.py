from flask_restful import Resource, reqparse


class BaseResource(Resource):
    def __init__(self):
        super(BaseResource, self).__init__()
        from backend import mongo
        self.mongo = mongo
        self.parser = reqparse.RequestParser()

    @staticmethod
    def clear_args(args):
        return {key: value for key, value in args.items() if value}