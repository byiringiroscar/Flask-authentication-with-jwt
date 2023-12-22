from flask import Flask
from extension import db
from auth import auth_bp


def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env()
    # initialize extension
    db.init_app(app)


    # register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    return app

