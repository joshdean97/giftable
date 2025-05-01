# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class GiftCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    balance = db.Column(db.Float, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<GiftCard {self.code} - Balance: {self.balance}>"
