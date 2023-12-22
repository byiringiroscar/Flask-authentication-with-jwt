from flask import Blueprint, jsonify, request
from models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.post('/register')
def register_user():
    data = request.get_json()
    username = data.get('username')
    user = User.get_user_by_username(username=username)
    if user is not None:
        pass
    else:
        return jsonify({"error": "User already exists"})
    email = data.get('email')
    return jsonify({'message': 'User created'})