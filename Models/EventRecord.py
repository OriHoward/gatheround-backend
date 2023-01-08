from server import db


class EventRecord(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    event_date = db.Column(db.DateTime)
    category = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100))
    description = db.Column(db.String(200))
    limit_attending = db.Column(db.Integer, default=100)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "event_date": self.event_date.strftime('%d/%m/%Y %H:%M'),
            "category" : self.category,
            "address": self.address,
            "description": self.description,
            "limit_attending": self.limit_attending
        }
