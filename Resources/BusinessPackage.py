from flask_restful import Resource, reqparse
from flask import request
from server import db
from Models.BusinessPackageRecord import BusinessPackageRecord
from flask_jwt_extended import get_jwt_identity, jwt_required


class BusinessPackage(Resource):

    @jwt_required()
    def get(self):
        """
        The get request returns the Packages created by the business user
        """
        parser = reqparse.RequestParser()
        parser.add_argument('package-limit', location='args')
        args = parser.parse_args()
        all_packages: BusinessPackageRecord = db.session.query(BusinessPackageRecord). \
            order_by(BusinessPackageRecord.price.desc()).limit(args.get("package-limit")).all()
        my_packages = list(map(lambda entry: entry.serialize(), all_packages))
        return {"my_packages": my_packages}

        pass

    @jwt_required()
    def post(self):
        """
        The post request inserts the data into the Package table
        """
        received_data = request.json
        business_id = get_jwt_identity().get("id")
        package_name = received_data.get("packageName")
        description = received_data.get("description")
        currency = received_data.get("currency")
        price = received_data.get("price")
        curr_package: BusinessPackageRecord = BusinessPackageRecord(user_id=business_id, package_name=package_name,
                                                                    description=description, currency=currency,
                                                                    price=price)

        db.session.add(curr_package)
        db.session.commit()

        return {'status': 'accepted'}

    @jwt_required()
    def put(self):
        pass
