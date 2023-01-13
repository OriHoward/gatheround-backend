from flask_restful import Resource
from Models.RequestRecord import RequestRecord
from Models.RequestNotifRecord import RequestNotifRecord
from Models.EventRecord import EventRecord
from Models.BusinessPackageRecord import BusinessPackageRecord
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from server import db
from flask import abort


def format_result(request, event):
    return {
        "id": request.get("id"),
        "package_id": request.get("package_id"),
        "event_id": request.get("event_id"),
        "description": request.get("description"),
        "request_status": request.get("request_status"),
        "event_name": event.get("name"),
        "event_date": event.get("event_date"),
        "event_category": event.get("category"),
        "event_address": event.get("address"),
    }


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

        user_id = get_jwt_identity().get('id')
        request_record: RequestRecord = RequestRecord(package_id=package_id,
                                                      event_id=event_id,
                                                      description=received_data.get("description", "")
                                                      )
        notif_record = RequestNotifRecord(updated_by=user_id, notify_user=business_id)
        db.session.begin_nested()
        db.session.add(request_record)
        db.session.commit()
        notif_record.request_id = request_record.id
        db.session.add(notif_record)
        db.session.commit()

        return 200

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity().get("id")
        requests = RequestRecord.query.join(EventRecord, EventRecord.id == RequestRecord.event_id) \
            .join(BusinessPackageRecord, RequestRecord.package_id == BusinessPackageRecord.id) \
            .filter(BusinessPackageRecord.user_id == user_id) \
            .with_entities(RequestRecord, EventRecord).all()
        formatted_requests = [format_result(req.serialize(), event.serialize()) for req, event in requests]
        return {"requests": formatted_requests}
