from flask import Flask #This is a package which creates the HTTP server
from flask_restful import Api #This is an extention to Flask which adds REST API + object abstraction
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy #This adds SQL alchemy support
from flask_cors import CORS

load_dotenv()

# https://flask-restful.readthedocs.io/en/latest/quickstart.html
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URL").strip()

CORS(app)
db = SQLAlchemy(app) # ORM = Object-relational mapping
app.app_context().push()
api = Api(app)



