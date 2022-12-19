from flask_restful import Resource
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required


class Refresh(Resource):
    @jwt_required(fresh=False, refresh=True)
    def post(self):
        """
        The post request refreshes the access token.
        """
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity, fresh=False)
        return jsonify(access_token=access_token)
