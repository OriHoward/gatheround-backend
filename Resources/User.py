from flask_restful import Resource
from flask import request
from Models.UserRecord import UserRecord
from Models.BusinessRecord import BusinessRecord
import bcrypt
from server import db

salt = bcrypt.gensalt()


class User(Resource):
    def get(self):
        return {"a": "1"}

    def post(self):
        received_data = request.json
        is_business: bool = received_data.get("isBusiness", False)
        curr_user = UserRecord(
            email=received_data.get("email"),
            password=bcrypt.hashpw(received_data.get("password").encode('utf-8'), salt),
            first_name=received_data.get("firstName"),
            last_name=received_data.get("lastName"),
        )

        if not is_business:
            db.session.add(curr_user)
            db.session.commit()
            return {'status': "accepted"}

        curr_business = BusinessRecord(
            id=curr_user.id,
            profession=received_data.get("profession"),
            country=received_data.get("country"),
            city=received_data.get("city"),
            phone_number=received_data.get("phoneNumber"),
            visible=received_data.get("visible"))

        db.session.begin_nested()

        # Insert the first object and commit the changes
        db.session.add(curr_user)
        db.session.commit()
        curr_business.id = curr_user.id
        # Insert the second object and commit the changes
        db.session.add(curr_business)
        db.session.commit()

        return {'status': "accepted"}
