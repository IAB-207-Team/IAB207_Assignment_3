from flask import Blueprint, Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user, UserMixin
from .models import Event, User
from . import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event_management.db'
app.config['SECRET_KEY'] = 'your-secret-key'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Define Event model
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ticket_count = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False)

# Create a blueprint
bp = Blueprint('main', __name__)

# Create a LoginManager instance
login_manager = LoginManager()

# Associate the LoginManager instance with your Flask application
login_manager.init_app(bp)

# Tell LoginManager the login view to redirect to if a user is not logged in
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    events = Event.query.all()
    return render_template('index.html', events=events)

@app.route('/events/<int:event_id>', methods=['GET'])
def event_details(event_id):
    event = Event.query.get(event_id)

    if event is None:
        return 'Event not found', 404

    return render_template('event_details.html', event=event)

@app.route('/events/<int:event_id>/book', methods=['GET','POST'])
@login_required
def book_tickets(event_id):
    event = Event.query.get(event_id)

    if event is None:
        return 'Event not found', 404

    if request.method == 'POST':
        if event.ticket_count == 0:
            event.status = 'Sold Out'
            db.session.commit()
            return 'Event is sold out'

        quantity = int(request.form['quantity'])
        if quantity > event.ticket_count:
            return 'Order cannot be placed. The quantity exceeds the available tickets.'

        new_ticket_count = event.ticket_count - quantity
        event.ticket_count = new_ticket_count
        if new_ticket_count == 0:
            event.status = 'Sold Out'
        db.session.commit()

        return 'Ticket booked successfully'

    return render_template('book_event.html', event=event)

@bp.route('/events/<int:event_id>/eventdesc')
def event_description(event_id):
    event = Event.query.get(event_id)

    if event is None:
        return 'Event not found', 404

    return render_template('eventdesc.html', event=event)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
