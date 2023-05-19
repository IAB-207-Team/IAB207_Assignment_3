from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.model, UserMixing):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    emailid = Column(String(100), nullable=False)
    password_hash = Column(String(255), nullable=False)


class Event(db.model):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    event_title = Column(String(80))
    date = Column(Date)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    description = Column(String(255))
    genre = Column(String(255))
    location = Column(String(255))
    Amount_of_Tickets = Column(Integer)
    event_Status = Column(String(255))
    ticket_Price = Column(Integer)
    image = Column(String(400))

    comments = relationship('Comment', backref='event')
    
class Comment(db.model):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    text = Column(String(400))
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    user_id = Column(Integer, ForeignKey('users.id'))
    event_id = Column(Integer, ForeignKey('events.id'))

    user = relationship('User', backref='comments')

#Need to Add a booked table to keep track of tickets
class Booking(db.model):
    __tablename__ = 'booking'
    
    order_id = Column(Integer)
    order_date = Column(Date)
    user_id = Column(Integer, ForeignKey('users.id'))
    event_id = Column(Integer, ForeignKey('events.id'))

    user_booking = relationship('User', backref='booking')
    event_booking = relationship('Event', backref='booking')

    def __repr__(self):
        return "<Comment: {}>".format(self.text)
