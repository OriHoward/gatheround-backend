from server import db
from datetime import datetime


class EventRecord(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_record.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100))
    event_date = db.Column(db.DateTime)
    description = db.Column(db.String(200))

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "address": self.address,
            "event_date": self.event_date,
            "description": self.description,
        }
