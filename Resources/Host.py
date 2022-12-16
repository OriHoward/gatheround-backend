from flask_restful import Resource
from flask import request
from Models.HostRecord import HostRecord
from server import db


class Host(Resource):
    def post(self):
        received_data = request.json

        curr_host = HostRecord(
            event_id=received_data.get("eventId"),
            user_id=received_data.get("userId"),  # host user id
        )

        db.session.add(curr_host)
        db.session.commit()

        return {'status': 'accepted'}
