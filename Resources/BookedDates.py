from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from Models.CalendarRecord import CalendarRecord
from server import db
from datetime import datetime


class BookedDates(Resource):

    @jwt_required()
    def post(self):
        received_data = request.json  # data sent from front is an array of dictionaries
        user_id = get_jwt_identity().get("id")
        for record in received_data:
            formatted_date = datetime.strptime(record.get("date"), '%d/%m/%Y')
            category = record.get("category")
            description = record.get("description")
            curr_calendar = CalendarRecord(user_id=user_id, date=formatted_date, category=category,
                                           description=description)
            db.session.add(curr_calendar)
            db.session.commit()
        return {'status': 'accepted'}

    @jwt_required()
    def get(self):
        pass
