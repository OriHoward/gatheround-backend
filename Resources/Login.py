from flask_restful import Resource
from flask import request
from Models.UserRecord import UserRecord
import bcrypt


class Login(Resource):

    def post(self):
        received_data = request.json
        user_found: UserRecord = UserRecord.query.filter_by(username=received_data.get("username")).first()
        received_pass = received_data.get("password").encode('utf-8')
        stored_pw = user_found.password.encode('utf-8')
        if bcrypt.checkpw(received_pass, stored_pw):
            print("this has to return a JWT")
            return {'status': "accepted"}, 202

        return {'status': "bad password"}, 401
