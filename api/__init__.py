from flask import Flask
from .config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from .models import db, GiftCard


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS

    db.init_app(app)

    # Create database tables
    @app.before_request
    def create_tables():
        db.create_all()

    @app.route("/")
    def home():
        return "Gift Card API Running!"

    # initt blueprints
    from .routes import gift_card_bp

    app.register_blueprint(gift_card_bp)

    return app
