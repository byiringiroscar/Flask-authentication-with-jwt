from flask import Flask, jsonify
from extension import db, jwt
from auth import auth_bp
from users import user_bp
from models import User, TokenBlocklist
import os

def create_app():
    app = Flask(__name__)
    db_path = os.path.join(os.getcwd(), 'instance', 'db.sqlite3')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    app.config.from_prefixed_env()
    # initialize extension
    db.init_app(app)
    jwt.init_app(app)


    # register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/users')

    # load user
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(username=identity).one_or_none()

    #additional claims
    @jwt.additional_claims_loader
    def make_additional_claims(identity):
        if identity == 'oscar':
            return {'is_staff': True}
        return {'is_staff': False}



    #jwt error handles
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        return jsonify({
            'message': 'Token has expired',
            'error': 'token_expired'
        }), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            'message': 'Signature verification failed',
            'error': 'invalid_token'
        }), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            'message': 'Request does not contain an access token',
            'error': 'authorization_required'
        }), 401
    
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
        jti = jwt_payload["jti"]
        token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

        return token is not None
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()


