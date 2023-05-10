from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__='users' # good practice to specify table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, unique=True, nullable=False)
	#password is never stored in the DB, an encrypted password is stored
	# the storage should be at least 255 chars long
    password_hash = db.Column(db.String(255), nullable=False)

    # relation to call user.comments and comment.created_by
    comments = db.relationship('Comment', backref='user')



class Events(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    event_title = db.Column(db.String(80))
    date = db.Column(db.Date)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    description = db.Column(db.String(255))
    genre = db.Column(db.String(255))
    #email = db.Column(db.String(100), index=True, nullable=False) <-- idk if we should have this
    location = db.Column(db.String(255))
    Amount_of_Tickets = db.Column(db.Integer)
    Ticket_Status = db.Column(db.String(255))
    Ticket_Price = db.Column(db.Integer)
    image = db.Column(db.String(400))
    # ... Create the Comments db.relationship
   
    comments = db.relationship('Comment', backref='event')
  

    
	
    def __repr__(self): #string print method
        return "<Name: {}>".format(self.name)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    #add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.String(100), db.ForeignKey('events.id'))


    def __repr__(self):
        return "<Comment: {}>".format(self.text)
