from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    emailid = db.Column(db.String(100), nullable=False)
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
    Amount_of_Tickets = db.Column(db.Integer)
    Ticket_Status = db.Column(db.String(255), default='Upcoming')
    Ticket_Price = db.Column(db.Integer)
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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    user_booking = db.relationship('User', backref='booking')
    event_booking = db.relationship('Event', backref='booking')

    def __repr__(self):
        return "<Comment: {}>".format(self.text)

    def __repr__(self):
        return "<Comment: {}>".format(self.text)
