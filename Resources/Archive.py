from flask_restful import Resource, reqparse
from flask import request
from Models.EventRecord import EventRecord
from Models.HostRecord import HostRecord
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime


class Archive(Resource):

    @jwt_required()
    def get(self):
        # RequestParser enables adding and parsing arguments of a single request
        parser = reqparse.RequestParser()
        parser.add_argument('host-limit', location='args')
        args = parser.parse_args()

        # get past events that user hosted
        curr_user_id = get_jwt_identity().get("id")
        response_data = dict()
        past_events_hosted: EventRecord = EventRecord.query.join(HostRecord) \
            .filter(HostRecord.user_id == curr_user_id, EventRecord.event_date <= datetime.now()) \
            .order_by(EventRecord.event_date).limit(args.get("host-limit", 10)).all()
        # if args.get("host-limit") is not provided- value is None and limit(None) returns all instances
        response_data["past_events"] = list(map(lambda entry: entry.serialize(), past_events_hosted))
        return response_data
