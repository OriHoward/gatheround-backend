from flask_restful import Resource
from Models.BusinessRecord import BusinessRecord
from flask_jwt_extended import jwt_required
from server import db


class BusinessSearchMetadata(Resource):
    @jwt_required()
    def get(self):
        try:
            distinct_professions_record: list[BusinessRecord] = db.session.query(
                BusinessRecord.profession).distinct().all()
            distinct_cities_record: list[BusinessRecord] = db.session.query(BusinessRecord.city).distinct().all()
            distinct_professions = [prof[0] for prof in distinct_cities_record]
            distinct_cities = [cityrec[0] for cityrec in distinct_professions_record]
            return {'results': {
                'distinctCities': distinct_cities,
                'distinctProfessions': distinct_professions
            }}
        except:
            return {}, 500
