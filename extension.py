from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import jwt_manager

db = SQLAlchemy()
jwt = jwt_manager()