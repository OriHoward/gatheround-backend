from flask_restful import Resource
from Models.InviteRecord import InviteRecord
from server import db
from flask import request


class Invite(Resource):

    def post(self):
        received_data = request.json
        curr_invite = InviteRecord(
            event_id=received_data.get("eventId"),
            user_id=received_data.get("userId"),
            is_attending=received_data.get("isAttending"),
            num_attending=received_data.get("numAttending"),
        )
        db.session.add(curr_invite)
        db.session.commit()
        print(received_data)
        return {'status': "accepted"}
