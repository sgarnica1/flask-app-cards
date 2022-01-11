from flask import Blueprint
from controllers.user_controller import index, add_user, delete_user, create_report

user_bp = Blueprint('user_bp', __name__)

user_bp.route('/<int:id>', methods=['GET'])(index)
user_bp.route('/add', methods=['GET', 'POST'])(add_user)
user_bp.route('/delete/<int:user_id>', methods=['DELETE', 'GET'])(delete_user)
user_bp.route('/report/<int:user_id>', methods=['GET'])(create_report)
