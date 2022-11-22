from flask_restful import Resource
from flask import request


class User(Resource):
    def get(self):
        return {"a": "1"}

    def post(self):
        received_data = request.json

        print(received_data)
        return {'status': "accepted"}
