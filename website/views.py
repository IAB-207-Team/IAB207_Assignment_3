from flask import Blueprint, render_template, request, redirect,url_for
from .models import booking

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    event = booking.query.all()    
    return render_template('index.html', event=event)

#Search Funcationality 
@bp.route('/search')
def search():
    if request.args['search']:
        print(request.args['search'])
        dest = "%" + request.args['search'] + '%'
        event = booking.query.filter(booking.description.like(booking)).all()
        return render_template('index.html', event=event)
    else:
        return redirect(url_for('main.index'))
