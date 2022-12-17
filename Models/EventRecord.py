from server import db


class EventRecord(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    event_date = db.Column(db.DateTime)
    address = db.Column(db.String(100))
    description = db.Column(db.String(200))
    limit_attending = db.Column(db.Integer, default=100)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "event_date": self.event_date.strftime('%d/%m/%Y'),
            "address": self.address,
            "description": self.description,
            "limit_attending": self.limit_attending
        }
