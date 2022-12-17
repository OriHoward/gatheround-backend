from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_restful import Resource
from flask import request
from Models.BusinessRecord import BusinessRecord
from server import db


class Business(Resource):
    @jwt_required()
    def get(self):
        curr_user = get_jwt_identity()
        business_info: BusinessRecord = BusinessRecord.query.filter_by(id=curr_user).first()
        return {"userId": business_info.id, "profession": business_info.profession,
                "country": business_info.country, "city": business_info.city,
                "phoneNumber": business_info.phone_number, "visible": business_info.visible}
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
