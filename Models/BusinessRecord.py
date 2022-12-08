from server import db


class BusinessRecord(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, foreign_key=True)
    profession = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    visible = db.Clumn(db.Boolean, default=True)

    def serialize(self):
        return {
            "id": self.id,
            "profession": self.profession,
            "country": self.country,
            "city": self.city,
            "phone_number": self.phone_number,
            "visible": self.visible
        }
