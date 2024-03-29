from server import db
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func


class RequestNotifRecord(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    request_id = db.Column(db.Integer, ForeignKey('request_record.id'))
    updated_by = db.Column(db.Integer, ForeignKey('user_record.id'))
    notify_user = db.Column(db.Integer, ForeignKey('user_record.id'))
    update_timestamp = db.Column(db.TIMESTAMP, nullable=False, server_default=func.now(),
                                 onupdate=func.current_timestamp())
    is_acknowledged = db.Column(db.Boolean, default=False, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "request_id": self.request_id,
            "updated_by": self.updated_by,
            "notify_user": self.notify_user,
            "update_timestamp": self.update_timestamp.timestamp() * 1000,
            # multiplication makes it so that parsing it works on javascript when passing to "new Date()"

        }
