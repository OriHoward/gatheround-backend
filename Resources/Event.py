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
        name = received_data.get("name")
        formatted_date = datetime.strptime(received_data.get("eventDate"), "%d/%m/%Y")
        address = received_data.get("address")
        description = received_data.get("description")
        limit_attending = received_data.get("limitAttending")
        curr_event: EventRecord = EventRecord(name=name, event_date=formatted_date, address=address,
                                              description=description, limit_attending=limit_attending)
        db.session.add(curr_event)
        db.session.commit()
        return {'status': "accepted", 'eventId': curr_event.id}

    def put(self):
        pass
