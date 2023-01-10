from flask_restful import Resource, reqparse
from flask import request
from Models.EventRecord import EventRecord
from Models.HostRecord import HostRecord
from Models.BusinessRecord import BusinessRecord
from datetime import datetime
from server import db
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required


class Event(Resource):
    @jwt_required()
    def get(self):
        """
        The get request returns events created by the Host user.
        """
        # RequestParser enables adding and parsing arguments of a single request
        parser = reqparse.RequestParser()
        parser.add_argument('host-limit', location='args')
        args = parser.parse_args()
        curr_user = get_jwt_identity()
        curr_user_id = curr_user.get("id")
        # check if user is a Host
        is_business: BusinessRecord = BusinessRecord.query.filter_by(id=curr_user_id).first() is not None
        response_data = dict()
        if is_business is False:
            # get events that user is hosting
            curr_events_hosting: EventRecord = EventRecord.query.join(HostRecord) \
                .filter(HostRecord.user_id == curr_user_id, EventRecord.event_date > datetime.now()) \
                .order_by(EventRecord.event_date).limit(args.get("host-limit", 10)).all()
            # if args.get("host-limit") is not provided- value is None and limit(None) returns all instances
            response_data["my_events"] = list(map(lambda entry: entry.serialize(), curr_events_hosting))
        return response_data

    @jwt_required()
    def post(self):
        """
        The post request inserts the data into the Event and Host Record tables (using a transaction).
        """
        received_data = request.json
        current_user = get_jwt_identity()

        name = received_data.get("name")
        formatted_date = datetime.strptime(received_data.get("eventDate"), '%d/%m/%Y %H:%M')
        category = received_data.get("categoryName")
        address = received_data.get("address")
        description = received_data.get("description")
        limit_attending = received_data.get("limitAttending")

        curr_event: EventRecord = EventRecord(name=name, event_date=formatted_date, category=category, address=address,
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

    @jwt_required()
    def delete(self, event_id):
        current_user = get_jwt_identity()
        user_id = current_user.get("id")
        # delete from Host table
        db.session.begin_nested()
        HostRecord.query.filter_by(event_id=event_id, user_id=user_id).delete()
        db.session.commit()
        EventRecord.query.filter_by(id=event_id).delete()
        db.session.commit()
        return {'status': 'accepted'}, 200

    def put(self):
        pass
