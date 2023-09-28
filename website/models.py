from . import db
from datetime import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'  # good practice to specify table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    contact_number = db.Column(db.String(12)) # Contact number a string so leading zeroes are not dropped
    address = db.Column(db.String(255))

    # # relation to call user.comments and comment.created_by
    # comments = db.relationship('Comment', backref='user')
