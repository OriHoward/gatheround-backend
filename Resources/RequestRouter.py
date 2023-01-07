from flask_restful import Resource
from Models.RequestRecord import RequestRecord
from flask import request
from flask_jwt_extended import jwt_required
from server import db
from flask import abort



class RequestRouter(Resource):
    @jwt_required()
    def post(self):
        received_data = request.json
        business_id = received_data.get("businessId")
        event_id = received_data.get("desiredEventId")
        package_id = received_data.get("packageId")
        if not business_id or not event_id or not package_id:
            abort(406)

        existing_record = RequestRecord.query.filter(RequestRecord.event_id == event_id,
                                                     RequestRecord.package_id == package_id).all()
        if len(existing_record) > 0:
            abort(409)
        print(existing_record)
        request_record: RequestRecord = RequestRecord(package_id=package_id,
                                                      event_id=event_id,
                                                      description=received_data.get("description", "")
                                                      )
        db.session.add(request_record)
        db.session.commit()
        return 200
