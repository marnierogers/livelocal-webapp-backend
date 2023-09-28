from . import db
from datetime import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'  # good practice to specify table name
    id = db.Column(db.Integer, index=True, unique=True, primary_key=True)
    name = db.Column(db.String(100), index=True, nullable=False)
    email_id = db.Column(db.String(100), index=True,
                         unique=True, nullable=False)
    
    password_hash = db.Column(db.String(255), nullable=False)
    contact_number = db.Column(db.String(12), nullable=False) # Contact number a string so leading zeroes are not dropped
    address_line1 = db.Column(db.String(255), nullable=False)
    suburb = db.Column(db.String(255), nullable=False)
    postcode = db.Column(db.Integer, nullable=False)

    # # relation to call user.comments and comment.created_by
    # comments = db.relationship('Comment', backref='user')
