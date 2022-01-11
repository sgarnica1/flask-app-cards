from flask import Blueprint
from controllers.cards_controller import *

cards_bp = Blueprint('cards_bp', __name__)

cards_bp.route('/<string:type>/<int:card_number>', methods=['GET'])(index)

# ADD CARD
cards_bp.route(
    '/add/<string:type>-card/user/<int:user_id>', methods=['GET'])(add_card_get)
cards_bp.route('/add/<string:type>-card', methods=['POST'])(add_card_post)

# DELETE CARD
cards_bp.route(
    '/delete/<string:type>-card/<int:id>', methods=['DELETE', 'GET'])(delete_card)
cards_bp.route(
    '/report/<string:type>/<string:card_number>', methods=['GET'])(create_report)

# RECALCULATE LOAN
cards_bp.route(
    '/recalculate-loan/credit/<string:card_number>', methods=['POST', 'GET'])(recalculate_loan)

# PAYEMTS
cards_bp.route(
    '/pay-total/<string:type_card>/<string:card_number>', methods=['POST'])(make_total_payment)
cards_bp.route(
    '/pay-partial/credit/<string:card_number>', methods=['POST'])(make_partial_payment)
