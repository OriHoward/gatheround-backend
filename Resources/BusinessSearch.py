from flask_restful import Resource, reqparse
from Models.BusinessRecord import BusinessRecord
from flask_jwt_extended import jwt_required


class BusinessSearch(Resource):
    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('profession', location='args', help='bad profession provided')
        args = parser.parse_args()
        # ilike is a case insensitive LIKE
        relevant_businesses: list[BusinessRecord] = BusinessRecord.query.filter(
            BusinessRecord.profession.ilike(f'%{args.get("profession")}%'),
            BusinessRecord.visible == True).all()
        return {'results': [entry.serialize() for entry in relevant_businesses]}
