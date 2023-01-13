from flask_restful import Resource
from Models.RequestRecord import RequestRecord
from Models.RequestNotifRecord import RequestNotifRecord
from Models.EventRecord import EventRecord
from Models.BusinessPackageRecord import BusinessPackageRecord
from Models.HostRecord import HostRecord
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from server import db
from flask import abort


def format_result(req, event, host):
    return {
        "id": req.get("id"),
        "event_user_id": host.get("user_id"),
        "package_id": req.get("package_id"),
        "event_id": req.get("event_id"),
        "description": req.get("description"),
        "request_status": req.get("request_status"),
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
            .join(HostRecord, HostRecord.event_id == EventRecord.id) \
            .filter(BusinessPackageRecord.user_id == user_id) \
            .with_entities(RequestRecord, EventRecord, HostRecord).all()
        formatted_requests = [format_result(req.serialize(), event.serialize(), host.serialize()) for req, event, host
                              in requests]
        return {"requests": formatted_requests}

    @jwt_required()
    def put(self):
        received_data = request.json
        request_id = received_data.get("id")
        updated_by = get_jwt_identity().get("id")
        notify_user = received_data.get("event_user_id")
        notify_fields = ["updated_by", "notify_user", "is_acknowledged"]
        curr_request: RequestRecord = RequestRecord.query.filter_by(id=request_id).first()
        curr_notify: RequestNotifRecord = RequestNotifRecord.query.filter_by(request_id=request_id).first()
        status = received_data.get("request_status")
        is_ack = received_data.get("is_acknowledged")
        try:
            db.session.begin_nested()
            setattr(curr_request, "request_status", status)
            setattr(curr_notify, notify_fields[0], updated_by)
            setattr(curr_notify, notify_fields[1], notify_user)
            setattr(curr_notify, notify_fields[2], is_ack)
            db.session.commit()
            db.session.commit()
            return {"request_status": status}
        except Exception as e:
            return {"status": "Failed"}
