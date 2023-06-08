from flask import Blueprint, render_template, request, redirect,url_for
from .models import Event

bp = Blueprint('main', __name__)

# allows for events to be viewed on the index page
@bp.route('/')
def index():
    events = Event.query.all()   # Queries all information in the Event table
    return render_template('index.html', events=events) #Renders the template with the queried information from Event and allows for it to be displayed

#Search Funcationality 
@bp.route('/search')
def search():
    if request.args['search']:
        print(request.args['search'])
        event = "%" + request.args['search'] + '%'
        event = Event.query.filter(Event.description.like(Event)).all()
        return render_template('index.html', event=event)
    else:
        return redirect(url_for('index'))
