from server import db
from sqlalchemy import ForeignKey


class CalendarRecord(db.Model):
    user_id = db.Column(db.Integer, ForeignKey('user_record.id'))
    date = db.Column(db.DateTime, nullable=False)
    category = db.Column(db.String, nullable=False)
    description = db.Column(db.String(200))

    def serializable(self):
        return {
            "user_id": self.user_id,
            "date": self.date,
            "category": self.category,
            "description": self.description
        }
