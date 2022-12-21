from server import db
from sqlalchemy import ForeignKey


class BusinessPackageRecord(db.Model):
    id = db.Column(db.Integer, ForeignKey('business_record.id'), primary_key=True)
    package_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
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
