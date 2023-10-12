from . import db
from datetime import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'  # good practice to specify table name
    id = db.Column(db.Integer, index=True, unique=True, primary_key=True, nullable=False)
    name = db.Column(db.String(100), index=True, nullable=False)
    email_id = db.Column(db.String(100), index=True,
                         unique=True, nullable=False)
    
    password_hash = db.Column(db.String(255), nullable=False)
    contact_number = db.Column(db.String(12), nullable=False) # Contact number a string so leading zeroes are not dropped
    address_line1 = db.Column(db.String(255), nullable=False)
    suburb = db.Column(db.String(255), nullable=False)
    postcode = db.Column(db.Integer, nullable=False)
    avatar = db.Column(db.String(400), nullable=False)

    # relation to call user.comments and comment.created_by
    comments = db.relationship('Comment', backref='user')
    experiences = db.relationship('Experience', backref='user', lazy=True)
    bookings = db.relationship('Booking', backref='user', lazy=True)


class Experience(db.Model):
    __tablename__ = 'experiences'
    id = db.Column(db.Integer, index=True, unique=True, primary_key=True)
    type = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(1500), nullable=False)

    address_line1 = db.Column(db.String(255), nullable=False)
    suburb = db.Column(db.String(255), nullable=False)
    postcode = db.Column(db.Integer, nullable=False)

    start_date = db.Column(db.String, nullable=False)
    start_time = db.Column(db.String, nullable=False)
    end_time = db.Column(db.String, nullable=False)
    ticket_qty = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    image_1 = db.Column(db.String(400), nullable=False)
    image_2 = db.Column(db.String(400), nullable=False)
    image_3 = db.Column(db.String(400), nullable=False)
    status = db.Column(db.String(20), default="Open", nullable=False)

    # ... Create the Comments db.relationship
    # relation to call destination.comments and comment.destination
    comments = db.relationship('Comment', backref='experience')

    # Create user db.relationship
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):  # string print method
        return f"Name: {self.name}"

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())

    #add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    experience_id = db.Column(db.Integer, db.ForeignKey('experiences.id'))

    def __repr__(self):
        return f"Comment: {self.text}"


class Booking(db.Model):
    __tablename__ = 'bookings'
    booking_id = db.Column(db.Integer, index=True, unique=True, primary_key=True)
    purchased_ticket_qty = db.Column(db.Integer, nullable=False)
    purchase_date = db.Column(db.String, nullable=False)

    #add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    experience_id = db.Column(db.Integer, db.ForeignKey('experiences.id'))
