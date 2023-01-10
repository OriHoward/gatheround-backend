from flask_restful import Resource
from flask_jwt_extended import jwt_required

from Models.RequestNotifRecord import RequestNotifRecord


class RequestNotifRouter(Resource):
    @jwt_required()
    def post(self):
        return 200
