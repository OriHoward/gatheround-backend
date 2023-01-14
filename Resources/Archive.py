from flask_restful import Resource, reqparse
from flask import request
from Models.EventRecord import EventRecord
from Models.HostRecord import HostRecord
from Models.BusinessRecord import BusinessRecord
from Models.RequestRecord import RequestRecord
from Models.BusinessPackageRecord import BusinessPackageRecord
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime


class Archive(Resource):

    @jwt_required()
    def get(self):
        # RequestParser enables adding and parsing arguments of a single request
        parser = reqparse.RequestParser()
        parser.add_argument('limit', location='args')
        args = parser.parse_args()

        curr_user_id = get_jwt_identity().get("id")
        # check if user is a Host
        is_business: BusinessRecord = BusinessRecord.query.filter_by(id=curr_user_id).first() is not None
        response_data = dict()
        response_data["past_events"] = list()
        if is_business is False:
            # get past events that user hosted
            past_events = EventRecord.query \
                .join(HostRecord) \
                .filter(HostRecord.user_id == curr_user_id, EventRecord.event_date <= datetime.now()) \
                .order_by(EventRecord.event_date) \
                .limit(args.get("limit", 10)).all()
            for event in past_events:
                event_dict = event.serialize()
                event_packages = BusinessPackageRecord.query \
                    .join(RequestRecord, BusinessPackageRecord.id == RequestRecord.package_id) \
                    .filter(RequestRecord.event_id == event.id) \
                    .all()
                package_dict = list(map(lambda entry: entry.serialize(), event_packages))
                response_data["past_events"].append({"event": event_dict, "packages": package_dict})
        return response_data
