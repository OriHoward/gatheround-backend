import os
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask  # This is a package which creates the framework for our web application (HTTP server)
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api  # This is an extension to Flask which adds REST API + object abstraction
from flask_sqlalchemy import SQLAlchemy  # This adds SQL alchemy support

load_dotenv()

# https://flask-restful.readthedocs.io/en/latest/quickstart.html
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URL").strip()
# If true this will only allow the cookies that contain your JWTs to be sent
# over https. In production, this should always be set to True
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

CORS(app)  # A security feature that blocks web pages from making requests to a different domains
db = SQLAlchemy(app)  # ORM = Object-relational mapping
app.app_context().push()
api = Api(app)  # A method in the Flask web framework that is used to push the application context onto the stack.
jwt = JWTManager(app)  # Adding JSON Web Token (JWT) authentication to a Flask application
