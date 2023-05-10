from flask import Blueprint, render_template, request, redirect,url_for
from .models import Events

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    destinations = Events.query.all()    
    return render_template('index.html', event=event)

@bp.route('/search')
def search():
    if request.args['search']:
        print(request.args['search'])
        dest = "%" + request.args['search'] + '%'
        event = Events.query.filter(Events.description.like(dest)).all()
        return render_template('index.html', event=event)
    else:
        return redirect(url_for('main.index'))
