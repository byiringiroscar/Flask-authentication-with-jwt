from flask import Blueprint, jsonify, request
from flask_jwt_extended import  (create_access_token, 
                                 create_refresh_token, 
                                 jwt_required, get_jwt, 
                                 current_user,
                                 get_jwt_identity
                                 )
from models import User, TokenBlocklist
from extension import db
from flasgger import swag_from

auth_bp = Blueprint('auth', __name__)

@auth_bp.post('/login')
@swag_from('./docs/auth/login.yaml')
def login_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username:
        return jsonify({"error": "Username is required"}), 400
    if not password:
        return jsonify({"error": "Password is required"}), 400
    user = User.get_user_by_username(username=username)
    if user is None:
        return jsonify({"error": "User does not exist"}), 404
    if not user.check_password(password=password):
        return jsonify({"error": "Invalid credentials"}), 403
    access_token = create_access_token(identity=user.username)
    refresh_token = create_refresh_token(identity=user.username)
    return jsonify(
        {
            'message': 'Logged In',
            'tokens': {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        }
    ), 200
    

@auth_bp.post('/register')
def register_user():
    data = request.get_json()
    username = data.get('username')
    user = User.get_user_by_username(username=username)
    if user is not None:
        return jsonify({"error": "User already exists"}), 403
    new_user = User(
        username=username,
        email=data.get('email')
    )

    new_user.set_password(data.get('password'))
    new_user.save()
    return jsonify({"message": "User created successfully"}), 201


@auth_bp.get('/whoami')
@jwt_required()
def whoami():
    return jsonify({
        'message': 'message',
        'user_details': {
            'username': current_user.username,
            'email': current_user.email
        }
    })


@auth_bp.get('/refresh')
@jwt_required(refresh=True)
def refresh_access():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    refresh_token = create_refresh_token(identity=identity)
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token
        })


@auth_bp.post('/logout')
@jwt_required(verify_type=False)
def logout_user():
    token = get_jwt()
    jti = token["jti"]
    ttype = token["type"]
    db.session.add(TokenBlocklist(jti=jti, type=ttype))
    db.session.commit()
    return jsonify({'message': 'Successfully logged out'}), 200