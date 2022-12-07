from flask_restful import Resource
from flask import request
from Models.UserRecord import UserRecord
import bcrypt
from server import db

salt = bcrypt.gensalt()


class User(Resource):
    def get(self):
        return {"a": "1"}

    def post(self):
        received_data = request.json

        curr_user = UserRecord(
            email=received_data.get("email"),
            password=bcrypt.hashpw(received_data.get("password").encode('utf-8'), salt),
            first_name=received_data.get("firstName"),
            last_name=received_data.get("lastName"),
        )
        db.session.add(curr_user)
        db.session.commit()
        print(received_data)
        return {'status': "accepted"}
