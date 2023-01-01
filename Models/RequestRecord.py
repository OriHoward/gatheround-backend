from server import db
from enum import Enum
from Models.UserRecord import UserRecord
from Models.EventRecord import EventRecord
from sqlalchemy import ForeignKey


class IsAttendingStatus(Enum):
    DECLINE = 0
    ACCEPT = 1
    PENDING = 2


class RequestRecord(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    package_id = db.Column(db.Integer, ForeignKey('business_package_record.id'))
    event_id = db.Column(db.Integer, ForeignKey('event_record.id'))
    description = db.Column(db.String(200), nullable=False)
    request_status = db.Column(db.Integer, default=IsAttendingStatus.PENDING)

    def serialize(self):
        return {
            "id": self.id,
            "package_id": self.package_id,
            "event_id": self.event_id,
            "description": self.description,
            "request_status": self.request_status,
        }
