from flask import request, jsonify, Blueprint

from .models import db, GiftCard

from .config import SQLALCHEMY_DATABASE_URI

# Initialize the Flask Blueprint
gift_card_bp = Blueprint("gift_card", __name__, url_prefix="/api/giftcards")


def create_gift_card_code():
    import random
    import string

    while True:
        code = "".join(random.choices(string.digits, k=10))
        if not GiftCard.query.filter_by(code=code).first():
            return code


# create a new gift card
@gift_card_bp.route("/create/", methods=["POST"])
def create_gift_card():
    balance = request.form.get("balance")
    if not balance or float(balance) <= 0:
        return jsonify({"error": "Invalid balance"}), 400
    code = create_gift_card_code()
    new_gift_card = GiftCard(code=code, balance=balance)
    db.session.add(new_gift_card)
    db.session.commit()
    return (
        jsonify({"message": "Gift card created", "code": code, "balance": balance}),
        201,
    )


# get all gift cards
@gift_card_bp.route("/", methods=["GET"])
def get_all_gift_cards():
    gift_cards = GiftCard.query.all()
    return jsonify([{"code": gc.code, "balance": gc.balance} for gc in gift_cards])


# get a gift card by id
@gift_card_bp.route("/<string:code>/", methods=["GET"])
def get_gift_card(code):
    gift_card = GiftCard.query.filter_by(code=code).first()
    if not gift_card:
        return jsonify({"error": "Gift card not found"}), 404
    return jsonify({"code": gift_card.code, "balance": gift_card.balance})


# redeem a gift card
@gift_card_bp.route("/redeem/<string:code>/", methods=["POST"])
def redeem_gift_card(code):
    gift_card = GiftCard.query.filter_by(code=code).first()
    if not gift_card:
        return jsonify({"error": "Gift card not found"}), 404
    amount = request.form.get("amount")
    if not amount or amount <= 0 or amount > gift_card.balance:
        return jsonify({"error": "Invalid amount"}), 400
    gift_card.balance -= amount
    db.session.commit()
    return jsonify({"message": "Gift card redeemed", "new_balance": gift_card.balance})
