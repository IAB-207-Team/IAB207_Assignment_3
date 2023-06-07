from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    user = db.relationship('Comment', backref='User')

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    event_title = db.Column(db.String(80))
    date = db.Column(db.Date)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    description = db.Column(db.String(255))
    genre = db.Column(db.String(255))
    location = db.Column(db.String(255))
    amount_of_tickets = db.Column(db.Integer)
    ticket_status = db.Column(db.String(255), default='Upcoming')
    ticket_price = db.Column(db.Integer)
    image = db.Column(db.String(400))
    
    comments = db.relationship('Comment', backref='Event')
    event_booking = db.relationship('Booking', backref='Event')

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, server_default='CURRENT_TIMESTAMP')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))


class Booking(db.Model):
    __tablename__ = 'booking'
    
    order_id = db.Column(db.Integer, autoincrement=True, primary_key =True)
    order_date = db.Column(db.Date, server_default='CURRENT_TIMESTAMP')
    email_id = db.Column(db.String(100), db.ForeignKey('users.email'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    total_price = db.Column(db.Integer)
    card_no = db.Column(db.String(16))
    expiry = db.Column(db.Date)
    CVV = db.Column(db.String(3))

    user_booking = db.relationship('User', backref='booking')
    event_booking = db.relationship('Event', backref='booking')

    def __repr__(self):
        return "<Comment: {}>".format(self.text)

    def __repr__(self):
        return "<Comment: {}>".format(self.text)
