from flask_restful import Resource
from flask import request
from Models.EventRecord import EventRecord
from Models.HostRecord import HostRecord
from datetime import datetime
from server import db
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required


class Event(Resource):
    def get(self):
        return {"a": "1"}

    @jwt_required()
    def post(self):
        received_data = request.json
        current_user = get_jwt_identity()

        name = received_data.get("name")
        formatted_date = datetime.strptime(received_data.get("eventDate"), "%d/%m/%Y")
        address = received_data.get("address")
        description = received_data.get("description")
        limit_attending = received_data.get("limitAttending")

        curr_event: EventRecord = EventRecord(name=name, event_date=formatted_date, address=address,
                                              description=description, limit_attending=limit_attending)
        host_record: HostRecord = HostRecord(event_id=curr_event.id, user_id=current_user.get("id"))

        # Start a transaction
        db.session.begin_nested()

        # Insert the first object and commit the changes
        db.session.add(curr_event)
        db.session.commit()
        host_record.event_id = curr_event.id
        # Insert the second object and commit the changes
        db.session.add(host_record)
        db.session.commit()
        return {'status': "accepted"}

    def put(self):
        pass
