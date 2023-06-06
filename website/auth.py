from flask import Blueprint, render_template, request,redirect,url_for,flash
from .forms import LoginForm, RegisterForm, CreateEvent, CommentForm, BookEvent
#new imports:
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User, Event, Comment
import os
from werkzeug.utils import secure_filename
from . import db

#create a blueprint
bp = Blueprint('auth', __name__ )

@bp.route('/register', methods=['GET', 'POST'])
def register():
    register = RegisterForm()
    #the validation of form submis is fine
    if (register.validate_on_submit() == True):
            #get username, password and email from the form
            uname =register.user_name.data
            pwd = register.password.data
            email = register.email_id.data
            #check if a user exists
            u1 = User.query.filter_by(name=uname).first()
            if u1:
                flash('User name already exists, please login')
                return redirect(url_for('auth.login'))
            # don't store the password - create password hash
            pwd_hash = generate_password_hash(pwd)
            #create a new user model object
            new_user = User(name=uname, password_hash=pwd_hash, email=email)
            db.session.add(new_user)
            db.session.commit()
            #commit to the database and redirect to HTML page
            return redirect(url_for('main.index'))
    #the else is called when there is a get message
    else:
        return render_template('user.html', form=register, heading='Register')


#authenticate against the user
@bp.route('/login', methods=['GET', 'POST'])
def login(): #view function
     print('In Login View function')
     login_form = LoginForm()
     error=None
     if(login_form.validate_on_submit()==True):
         email = login_form.email_id.data
         password = login_form.password.data
         user = User.query.filter_by(name=email).first()
         if user is None:
             error='Incorrect credentials supplied'
         elif not check_password_hash(user.password_hash, password): # takes the hash and password
             error='Incorrect credentials supplied'
         if error is None:
             login_user(user)
             nextp = request.args.get('next') #this gives the url from where the login page was accessed
             print(nextp)
             return render_template('index.html', form=login_form, heading='Login')
         else:
             flash(error)
     return render_template('user.html', form=login_form, heading='Login')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('logoutscreen.html', heading='Logged Out')

@bp.route('/<id>')
def show(id):
    destination = Event.query.filter_by(id=id).first()
    # create the comment form
    cform = CommentForm()    
    return render_template('eventdesc.html', destination=destination, form=cform)

@bp.route('/create', methods = ['GET', 'POST'])
@login_required
def create():
  print('Method type: ', request.method)
  form = CreateEvent()
  if form.validate_on_submit():
    #call the function that checks and returns image
    db_file_path=check_upload_file(form)
    destination=Event(event_title=form.event_title.data, date=form.date.data, start_time=form.start_time.data,end_time=form.end_time.data, description=form.description.data, genre=form.genre.data, location=form.location.data, amount_of_tickets=form.amount_of_tickets.data, ticket_price=form.ticket_price.data,image=db_file_path)
    # add the object to the db session
    db.session.add(destination)
    # commit to the database
    db.session.commit()
    print('Successfully created new travel destination', 'success')
    #Always end with redirect when form is valid
    return redirect(url_for('auth.create'))
  return render_template('user.html', form=form)

def check_upload_file(form):
  #get file data from form  
  fp=form.image.data
  filename=fp.filename
  #get the current path of the module file… store image file relative to this path  
  BASE_PATH=os.path.dirname(__file__)
  #upload file location – directory of this file/static/image
  upload_path=os.path.join(BASE_PATH,'static\images',secure_filename(filename))
  #store relative path in DB as image location in HTML is relative
  db_upload_path='\static\images\\' + secure_filename(filename)
  #save the file and return the db upload path  
  fp.save(upload_path)
  return db_upload_path

@bp.route('/<destination>/comment', methods = ['GET', 'POST'])  
@login_required
def comment(destination):  
    form = CommentForm()  
    #get the destination object associated to the page and the comment
    destination_obj = Event.query.filter_by(id=destination).first()  
    if form.validate_on_submit():  
      #read the comment from the form
      comment = Comment(text=form.text.data,  
                        destination=destination_obj,
                        user=current_user) 
      #here the back-referencing works - comment.destination is set
      # and the link is created
      db.session.add(comment) 
      db.session.commit() 

      #flashing a message which needs to be handled by the html
      #flash('Your comment has been added', 'success')  
      print('Your comment has been added', 'success') 
    # using redirect sends a GET request to destination.show
    return redirect(url_for('auth.show', id=destination))



@bp.route('/events', methods=['GET', 'POST'])

def book_event(event_id):
    form = BookEvent()
    event_id = form.id.data
    if form.validate_on_submit():
    #read the comment from the form
        book = BookEvent(email=form.email.id.data, card_no = form.card_no.data, expiry = form.expiry.data, CVV = form.CVV.data)
    

    if book is None:
        return 'Event not found', 404

    if request.method == 'POST' 'GET':
        if Event.ticket_count == 0:
            Event.status = 'Sold Out'
            db.session.commit()
            return 'Event is sold out'

        quantity = int(request.form['quantity'])
        if quantity > Event.ticket_count:
            return 'Order cannot be placed. The quantity exceeds the available tickets.'

        new_ticket_count = Event.ticket_count - quantity
        Event.ticket_count = new_ticket_count
        if new_ticket_count == 0:
            Event.status = 'Sold Out'
            db.session.commit()

        else:
            return redirect(url_for('booking.book_event'))
    return render_template('book_event.html', event=Event)

@bp.route('/<id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    chosenevent = Event.query.filter_by(id=id).first()

    form = UpdateEvent(obj=chosenevent)
    if form.validate_on_submit():
        # Call the function that checks and returns image
        db_file_path = check_upload_file(form)
        form.populate_obj(chosenevent)
        # Using https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/queries/
        chosenevent.event_title = form.event_title.data
        chosenevent.date = form.date.data
        chosenevent.start_time = form.start_time.data
        chosenevent.end_time = form.end_time.data
        chosenevent.description = form.description.data
        chosenevent.genre = form.genre.data
        chosenevent.location = form.location.data
        chosenevent.amount_of_tickets = form.amount_of_tickets.data
        chosenevent.ticket_price = form.ticket_price.data
        chosenevent.image = db_file_path
        chosenevent.ticket_status = form.ticket_status.data
        
        # Commit the changes to the database
        db.session.add(chosenevent)
        db.session.commit()

        print('Successfully updated event details', 'success')
        # Always end with a redirect when form is valid
        return redirect(url_for('main.index'))

    return render_template('user.html', form=form)
