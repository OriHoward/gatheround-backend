from flask_restful import Resource
from Models.RequestRecord import RequestRecord
from flask import request
from flask_jwt_extended import jwt_required
from server import db


class RequestRouter(Resource):
    @jwt_required()
    def post(self):
        received_data = request.json
        business_id = received_data.get("businessId")
        event_id = received_data.get("desiredEventId")
        package_id = received_data.get("packageId")
        if not business_id or not event_id or not package_id:
            return 406

        request_record: RequestRecord = RequestRecord(package_id=package_id,
                                                      event_id=event_id,
                                                      description=received_data.get("description", "")
                                                      )
        db.session.add(request_record)
        db.session.commit()
        return 200
