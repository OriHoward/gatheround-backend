from flask_restful import Resource
from flask import request
from server import db
from Models.BusinessPackageRecord import BusinessPackageRecord
from flask_jwt_extended import get_jwt_identity, jwt_required


class BusinessPackage(Resource):

    @jwt_required()
    def get(self):
        business_id = get_jwt_identity().get("id")
        pass

    @jwt_required()
    def post(self):
        received_data = request.json
        business_id = get_jwt_identity().get("id")
        package_name = received_data.get("packageName")
        description = received_data.get("description")
        currency = received_data.get("currency")
        price = received_data.get("price")
        curr_package: BusinessPackageRecord = BusinessPackageRecord(id=business_id, package_name=package_name,
                                                                    description=description, currency=currency,
                                                                    price=price)

        db.session.add(curr_package)
        db.session.commit()

        return {'status': 'accepted'}

    @jwt_required()
    def put(self):
        pass
