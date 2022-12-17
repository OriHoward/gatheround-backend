from flask_restful import Resource
from flask import request
from Models.UserRecord import UserRecord
from Models.BusinessRecord import BusinessRecord
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
        is_business: BusinessRecord = BusinessRecord.query.filter_by(id=user_found.id).first() is not None
        received_pass = received_data.get("password").encode('utf-8')
        stored_pw = user_found.password.encode('utf-8')
        if bcrypt.checkpw(received_pass, stored_pw):
            token_data = user_found.serialize()
            token_data['is_business'] = is_business
            access_token = create_access_token(identity=token_data, fresh=True)
            refresh_token = create_refresh_token(identity=token_data)
            response = jsonify(access_token=access_token, refresh_token=refresh_token, is_business=is_business)
            set_access_cookies(response, access_token)
            return response

        return {'status': "bad password"}, 401
