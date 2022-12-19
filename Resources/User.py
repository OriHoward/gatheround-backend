from flask_restful import Resource
from flask import request
from Models.UserRecord import UserRecord
from Models.BusinessRecord import BusinessRecord
import bcrypt
from server import db
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

salt = bcrypt.gensalt()


class User(Resource):

    @jwt_required()
    def get(self):
        """
        The get request returns the user's information.
        """
        user_id = get_jwt_identity().get('id')
        curr_user: UserRecord = UserRecord.query.filter_by(id=user_id).first()
        return curr_user.serialize()

    def post(self):
        """
        The post request happens when a new user is created.
        """
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

        # start a transaction: if either insertions were unsuccessful- will rollback changes
        db.session.begin_nested()

        # Insert the first object and commit the changes
        db.session.add(curr_user)
        db.session.commit()
        curr_business.id = curr_user.id
        # Insert the second object and commit the changes
        db.session.add(curr_business)
        db.session.commit()

        return {'status': "accepted"}

    @jwt_required()
    def put(self):
        """
        The put request updates the user's information in the database.
        """
        received_data = request.json
        user_id = get_jwt_identity().get('id')
        curr_user: UserRecord = UserRecord.query.filter_by(id=user_id).first()
        curr_user.first_name = received_data.get('firstName')
        curr_user.last_name = received_data.get('lastName')
        curr_user.email = received_data.get('email')
        db.session.commit()
        return {"status": "accepted"}
