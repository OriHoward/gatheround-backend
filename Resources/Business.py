from flask_restful import Resource
from flask import request
from Models.BusinessRecord import BusinessRecord
from server import db


class Business(Resource):
    def get(self):
        return {"b": "2"}

    def post(self):
        received_data = request.json
        curr_business = BusinessRecord(
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
