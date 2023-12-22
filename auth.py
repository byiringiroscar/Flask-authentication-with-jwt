from flask import Blueprint, jsonify, request
from models import User

auth_bp = Blueprint('auth', __name__)


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
    