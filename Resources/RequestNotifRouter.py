from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from Models.RequestNotifRecord import RequestNotifRecord
from Models.RequestRecord import RequestRecord
from Models.EventRecord import EventRecord
from server import db
from flask import abort


def format_result(notif, event):
    return {
        "id": notif.get("id"),
        "request_id": notif.get("request_id"),
        'event_name': event.get("name"),
        'event_date': event.get('event_date'),
        'address': event.get("address")
    }


class RequestNotifRouter(Resource):
    @jwt_required()
    def post(self):
        return 200

    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        notifs = RequestNotifRecord.query \
            .join(RequestRecord, RequestRecord.id == RequestNotifRecord.request_id) \
            .join(EventRecord, RequestRecord.event_id == EventRecord.id) \
            .filter(
            RequestNotifRecord.is_acknowledged == False, RequestNotifRecord.notify_user == current_user.get("id")) \
            .with_entities(EventRecord, RequestNotifRecord).all()
        formatted_notifs = [format_result(notif.serialize(), event.serialize()) for event, notif in notifs]
        return {"notification": formatted_notifs}

    @jwt_required()
    def put(self):
        try:
            body = request.json
            record: RequestNotifRecord = RequestNotifRecord.query \
                .filter_by(id=body.get("notifId")).first()
            record.is_acknowledged = True
            db.session.commit()
            return {"status": "updated"}
        except:
            abort(500)
