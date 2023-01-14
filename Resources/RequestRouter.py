from flask_restful import Resource, reqparse
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
        parser = reqparse.RequestParser()
        parser.add_argument('accepted-only', location='args')
        args = parser.parse_args()
        args_value = args.get('accepted-only')
        user_id = get_jwt_identity().get("id")
        requests = RequestRecord.query.join(EventRecord, EventRecord.id == RequestRecord.event_id) \
            .join(BusinessPackageRecord, RequestRecord.package_id == BusinessPackageRecord.id) \
            .join(HostRecord, HostRecord.event_id == EventRecord.id)
        if args_value is None:
            results = requests.filter(BusinessPackageRecord.user_id == user_id) \
                .with_entities(RequestRecord, EventRecord, HostRecord).all()
        else:  # get only accepted requests
            results = requests.filter(BusinessPackageRecord.user_id == user_id, RequestRecord.request_status == 1) \
                .with_entities(RequestRecord, EventRecord, HostRecord).all()
        formatted_requests = [format_result(req.serialize(), event.serialize(), host.serialize()) for req, event, host
                              in results]
        return {"requests": formatted_requests}

    @jwt_required()
    def put(self):
        received_data = request.json
        request_id = received_data.get("id")
        updated_by = get_jwt_identity().get("id")
        notify_user = received_data.get("event_user_id")
        curr_request: RequestRecord = RequestRecord.query.filter_by(id=request_id).first()
        new_notify: RequestNotifRecord = RequestNotifRecord(request_id=request_id, updated_by=updated_by
                                                            , notify_user=notify_user)
        status = received_data.get("request_status")

        try:
            db.session.begin_nested()
            setattr(curr_request, "request_status", status)
            db.session.add(new_notify)
            db.session.commit()
            db.session.commit()
            return {"request_status": status}
        except Exception as e:
            return {"status": "Failed"}
