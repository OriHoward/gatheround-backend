from server import db
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func


class RequestNotifRecord(db.Model):
    id = db.Column(db.Integer, ForeignKey('request_record.id'), default=0, primary_key=True)
    updated_by = db.Column(db.Integer, ForeignKey('user_record.id'))
    notify_user = db.Column(db.Integer, ForeignKey('user_record.id'))
    update_timestamp = db.Column(db.TIMESTAMP, nullable=False, server_default=func.now(),
                                 onupdate=func.current_timestamp())
    is_acknowledged = db.Column(db.Boolean, default=False, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "updated_by": self.updated_by,
            "notify_user": self.notify_user,
            "update_timestamp": self.update_timestamp,

        }
