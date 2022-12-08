from server import db
from enum import Enum
from Models.UserRecord import UserRecord
from sqlalchemy import ForeignKey


class IsAttendingStatus(Enum):
    DECLINE = 0
    PENDING = 1
    ACCEPT = 2


class InviteRecord(db.Model):
    event_id = db.Column(db.Integer, ForeignKey('event_record.id'), primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user_record.id'), primary_key=True)
    is_attending = db.Column(db.Integer, nullable=False, default=IsAttendingStatus.PENDING)
    num_attending = db.Column(db.Integer, nullable=False, default=0)

    def serialize(self):
        return {
            "event_id": self.event_id,
            "user_id": self.user_id,
            "is_attending": self.is_attending,
            "num_attending": self.num_attending,
        }
