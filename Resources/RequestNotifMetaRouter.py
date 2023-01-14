from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from Models.RequestNotifRecord import RequestNotifRecord


class RequestNotifMetaRouter(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        notif_count = RequestNotifRecord.query \
            .filter(RequestNotifRecord.is_acknowledged == False,
                    RequestNotifRecord.notify_user == current_user.get("id")).count()
        return {"notifCount": notif_count}
