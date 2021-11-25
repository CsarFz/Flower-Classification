from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    flowers = db.relationship("Flower", backref="user", passive_deletes=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class Flower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    path = db.Column(db.String(300), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())