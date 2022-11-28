from flask_restful import Resource
from flask import request
from Models.EventRecord import EventRecord
from datetime import datetime
from server import db


class Event(Resource):
    def get(self):
        return {"a": "1"}

    def post(self):
        received_data = request.json
        user_id = received_data.get("user_id")
        name = received_data.get("name")
        address = received_data.get("address")
        description = received_data.get("description")
        formated_date = datetime.strptime(received_data.get("event_date"), "%d/%m/%Y")
        curr_event: EventRecord = EventRecord(user_id=user_id, name=name, address=address, event_date=formated_date,
                                              description=description)
        db.session.add(curr_event)
        db.session.commit()
        return {'status': "accepted"}
