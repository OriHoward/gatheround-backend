from flask_restful import Resource
from flask import request, jsonify
from Models.UserRecord import UserRecord
from Jwt.jwt_handler import generate_jwt
import bcrypt


class Login(Resource):

    def post(self):
        received_data = request.json
        username = received_data.get("username")
        user_found: UserRecord = UserRecord.query.filter_by(username=username).first()
        received_pass = received_data.get("password").encode('utf-8')
        stored_pw = user_found.password.encode('utf-8')
        if bcrypt.checkpw(received_pass, stored_pw):
            token = generate_jwt(payload=received_data, lifetime=1)
            return jsonify({"data": token, "status": 200})

        return {'status': "bad password"}, 401
