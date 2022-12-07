from flask_restful import Resource
from flask import request
from Models.UserRecord import UserRecord
# from Jwt.jwt_handler import generate_jwt
import bcrypt
from flask_jwt_extended import create_access_token
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import create_refresh_token
from flask import jsonify


class Login(Resource):

    def post(self):
        received_data = request.json
        email = received_data.get("email")
        user_found: UserRecord = UserRecord.query.filter_by(email=email).first()
        received_pass = received_data.get("password").encode('utf-8')
        stored_pw = user_found.password.encode('utf-8')
        if bcrypt.checkpw(received_pass, stored_pw):
            access_token = create_access_token(identity=user_found.serialize(), fresh=True)
            refresh_token = create_refresh_token(identity=user_found.serialize())
            response = jsonify(access_token=access_token, refresh_token=refresh_token)
            set_access_cookies(response, access_token)
            return response

        return {'status': "bad password"}, 401
