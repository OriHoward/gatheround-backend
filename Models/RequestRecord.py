from server import db
from enum import Enum
from Models.UserRecord import UserRecord
from sqlalchemy import ForeignKey


class IsAttendingStatus(Enum):
    DECLINE = 0
    ACCEPT = 1
    PENDING = 2


class RequestRecord(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    business_id = db.Column(db.Integer, ForeignKey('business_record.id'))
    host_id = db.Column(db.Integer, ForeignKey('user_record.id'))
    package_id = db.Column(db.Integer, ForeignKey('business_package_record.id'))
    description = db.Column(db.String(200), nullable=False)
    request_status = db.Column(db.Integer, default=IsAttendingStatus.PENDING)

    def serialize(self):
        return {
            "id": self.id,
            "business_id": self.business_id,
            "host_id": self.host_id,
            "package_id": self.package_id,
            "description": self.description,
            "request_status": self.request_status,
        }
