from flask import Blueprint, render_template, request,redirect,url_for,flash
from .forms import LoginForm, RegisterForm
#new imports:
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User
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
    return 'You have been logged out'
