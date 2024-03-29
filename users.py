from flask import Blueprint, request, jsonify
from models import User
from schemas import UserSchema
from flask_jwt_extended import jwt_required, get_jwt
from flasgger import swag_from

user_bp = Blueprint('users', __name__)


@user_bp.get('/all')
@jwt_required()
def get_all_users():
    claims = get_jwt()
    if not claims['is_staff']:
        return jsonify({
            'message': 'You are not authorized to perform this action'
        }), 403
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=3, type=int)
    users = User.query.paginate(
            page=page,
            per_page=per_page
    )

    result = UserSchema().dump(users, many=True)
    return jsonify({
        'users': result,
    }), 200


@user_bp.get('/<string:username>')
@jwt_required()
@swag_from('./docs/user/user_single.yaml')
def get_user(username):
    user = User.get_user_by_username(username=username)
    if user is None:
        return jsonify({
            'message': 'User does not exist'
        }), 404
    result = UserSchema().dump(user)
    return jsonify({
        'user': result
    }), 200




