from server import db
from sqlalchemy import ForeignKey


class BusinessRecord(db.Model):
    id = db.Column(db.Integer, ForeignKey('user_record.id'), default=0, primary_key=True)
    profession = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    visible = db.Column(db.Boolean, default=True)

    def serialize(self):
        return {
            "id": self.id,
            "profession": self.profession,
            "country": self.country,
            "city": self.city,
            "phone_number": self.phone_number,
            "visible": self.visible
        }
