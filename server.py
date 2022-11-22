from flask import Flask
from flask_restful import Resource, Api, reqparse
from Resources.Event import Event
from Resources.User import User
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


load_dotenv()

# https://flask-restful.readthedocs.io/en/latest/quickstart.html
app = Flask(__name__)
CORS(app)
print(os.getenv("DB_URL"))
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URL")
db = SQLAlchemy(app) # ORM = Object-relational mapping
api = Api(app)


api.add_resource(Event, '/events')
api.add_resource(User, '/users')



if __name__ == '__main__':
    app.run(debug=True)
