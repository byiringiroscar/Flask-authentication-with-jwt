from flask import Blueprint, jsonify, request
from flask_jwt_extended import  create_access_token, create_refresh_token, jwt_required, get_jwt
from models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.post('/login')
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
    claims = get_jwt()
    return jsonify({
        'message': 'message',
        'claims': claims
    })