from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from Models.RequestNotifRecord import RequestNotifRecord
from Models.RequestRecord import RequestRecord
from Models.EventRecord import EventRecord


def format_result(notif, event):
    return {
        "id": notif.get("id"),
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
            .join(RequestRecord, RequestRecord.id == RequestNotifRecord.id) \
            .join(EventRecord, RequestRecord.event_id == EventRecord.id) \
            .filter(
            RequestNotifRecord.is_acknowledged == False, RequestNotifRecord.notify_user == current_user.get("id")) \
            .with_entities(EventRecord, RequestNotifRecord).all()
        formatted_notifs = [format_result(notif.serialize(), event.serialize()) for event, notif in notifs]
        return {"notification": formatted_notifs}
