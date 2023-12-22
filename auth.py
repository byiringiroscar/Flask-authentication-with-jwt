from flask import Blueprint, jsonify

auth_bp = Blueprint('auth', __name__)


@auth_bp.post('/register')
def register_user():
    return jsonify({'message': 'User created'})