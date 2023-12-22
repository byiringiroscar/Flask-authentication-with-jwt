from flask import Flask
from extension import db, jwt
from auth import auth_bp
from users import user_bp

def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env()
    # initialize extension
    db.init_app(app)
    jwt.init_app(app)


    # register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/users')
    return app

