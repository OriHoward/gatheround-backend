from server import db
from sqlalchemy import ForeignKey


class BusinessPackageRecord(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("user_record.id"))
    package_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000))
    price = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(3), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "package_name": self.package_name,
            "description": self.description,
            "currency": self.currency,
            "price": self.price
        }
