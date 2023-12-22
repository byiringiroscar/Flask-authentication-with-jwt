from flask import Blueprint, request
from models import User

user_bp = Blueprint('users', __name__)


@user_bp.get('/all')
def get_all_users():
    page = request.args.get('page', default=1)

    users = User.query.paginate(
            page=page,
            per_page=per_page
    )