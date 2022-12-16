from server import db
from Models.EventRecord import EventRecord
from Models.UserRecord import UserRecord
from sqlalchemy import ForeignKey


class HostRecord(db.Model):
    """
    This table holds the information of the host of an event.
    """
    event_id = db.Column(db.Integer, ForeignKey('event_record.id'), primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user_record.id'), primary_key=True)

    def serialize(self):
        return {
            "event_id": self.event_id,
            "user_id": self.user_id,
        }
