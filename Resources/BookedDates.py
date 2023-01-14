from flask_restful import Resource, reqparse
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
        dates = set()
        for record in received_data:
            formatted_date = datetime.strptime(record.get("date"), '%d/%m/%Y')
            dates.add(formatted_date)
            category = record.get("category")
            description = record.get("description")
            # check if record is in calendar (frontend sends all dates that are marked)
            is_booked = CalendarRecord.query.filter_by(user_id=user_id, date=formatted_date).first()
            if is_booked is None:
                curr_calendar = CalendarRecord(user_id=user_id, date=formatted_date, category=category,
                                               description=description)
                db.session.add(curr_calendar)
                db.session.commit()

        # delete dates that were unselected
        records = CalendarRecord.query.filter_by(user_id=user_id).all()
        for entry in records:
            if entry.date not in dates:
                CalendarRecord.query.filter_by(user_id=user_id, date=entry.date).delete()
                db.session.commit()

        return {'status': 'accepted'}

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity().get("id")
        booked_dates = CalendarRecord.query \
            .filter(CalendarRecord.user_id == user_id, CalendarRecord.date > datetime.now()) \
            .order_by(CalendarRecord.date).all()
        response_data = [record.serialize() for record in booked_dates]
        return response_data
