from server import db
from sqlalchemy import ForeignKey


class CalendarRecord(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)  # unique ID for entries
    user_id = db.Column(db.Integer, ForeignKey('user_record.id'))
    date = db.Column(db.DateTime, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "date": self.date.strftime('%d/%m/%Y'),
            "category": self.category,
            "description": self.description
        }
