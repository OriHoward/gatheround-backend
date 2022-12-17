from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_restful import Resource
from flask import request
from Models.BusinessRecord import BusinessRecord
from Models.UserRecord import UserRecord
from server import db


class Business(Resource):
    @jwt_required()
    def get(self):
        curr_user = get_jwt_identity()
        user_id = curr_user.get("id")
        user_record: UserRecord = UserRecord.query.filter_by(id=user_id).first()
        business_record: BusinessRecord = BusinessRecord.query.filter_by(id=user_record.id).first()
        return {"userRecord": user_record.serialize(), "businessRecord": business_record.serialize()}

    def post(self):
        received_data = request.json
        curr_business = BusinessRecord(
            id=received_data.get("userId"),
            profession=received_data.get("profession"),
            country=received_data.get("country"),
            city=received_data.get("city"),
            phone_number=received_data.get("phoneNumber"),
            visible=received_data.get("visible"))
        db.session.add(curr_business)
        db.session.commit()
        print(received_data)
        return {"status": "accepted"}

    def put(self):
        pass

    def delete(self):
        pass
