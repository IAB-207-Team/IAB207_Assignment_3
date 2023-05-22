from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.model, db.UserMixing):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    emailid = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)


class Event(db.model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_title = db.Column(db.String(80))
    date = db.Column(db.Date)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    description = db.Column(db.String(255))
    genre = db.Column(db.String(255))
    location = db.Column(db.String(255))
    Amount_of_Tickets = db.Column(db.Integer)
    event_Status = db.Column(db.String(255), default='Upcoming Event')
    ticket_Price = db.Column(db.Integer)
    image = db.Column(db.String(400))

    comments = db.relationship('Comment', backref='event')
    
class Comment(db.model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, server_default='CURRENT_TIMESTAMP')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    user = db.relationship('User', backref='comments')

#Need to Add a booked table to keep track of tickets
class Booking(db.model):
    __tablename__ = 'booking'
    
    order_id = db.Column(db.Integer, autoincrement=True)
    order_date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    user_booking = db.relationship('User', backref='booking')
    event_booking = db.relationship('Event', backref='booking')

    def __repr__(self):
        return "<Comment: {}>".format(self.text)
