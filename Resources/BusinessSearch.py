from flask_restful import Resource, reqparse
from Models.BusinessRecord import BusinessRecord
from Models.BusinessPackageRecord import BusinessPackageRecord
from flask_jwt_extended import jwt_required


class BusinessSearch(Resource):
    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('desiredProfession', location='args', help='bad profession provided')
        parser.add_argument('city', location='args', help='bad city provided')
        args = parser.parse_args()
        relevant_businesses: list = BusinessRecord.query \
            .join(BusinessPackageRecord, BusinessRecord.id == BusinessPackageRecord.user_id).filter(
            BusinessRecord.visible == True)

        if args.get("desiredProfession"):
            relevant_businesses = relevant_businesses.filter(
                BusinessRecord.profession.ilike(f'%{args.get("desiredProfession")}%'))
        if args.get("city"):
            relevant_businesses = relevant_businesses.filter(BusinessRecord.city.ilike(f'%{args.get("city")}%'))

        relevant_businesses = relevant_businesses.with_entities(BusinessRecord, BusinessPackageRecord).all()
        return {'results': [{**(bus_entry.serialize()), **(packge_entry.serialize())} for bus_entry, packge_entry in
                            relevant_businesses]}
