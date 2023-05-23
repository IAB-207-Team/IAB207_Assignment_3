
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILE = {'PNG','JPG','png','jpg'}

#Create new event
class CreateEvent(FlaskForm):
    event_title = StringField('Event Title', validators=[InputRequired()])
    date = DateField('Start Date', format='%d/%m/%Y')
    start_time = TimeField('Start Time')
    end_time = TimeField('End Time')
    description = TextAreaField('Description', validators=[InputRequired()])
    genre = StringField('Genre')
    location = TextAreaField('Mailing Address', validators=[InputRequired()])
    amount_of_tickets = IntegerField('Amount')
    ticket_price =DecimalField('Price', places=2, render_kw={'TIcket Price': 'Enter the ticket price'})
    image = FileField('Destination Image', validators=[FileRequired(message='Image cannot be empty'), FileAllowed(ALLOWED_FILE, message='Only supports png,jpg,JPG,PNG')])
    submit = SubmitField('Create')
    


#creates the login information
class LoginForm(FlaskForm):
    email_id=StringField("Email Address", validators=[InputRequired('Enter email')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    #submit button
    submit = SubmitField("Register")

class CommentForm(FlaskForm):
    text = TextAreaField("Comment", validators=[InputRequired(), Length(min=10, max=200, message="Comment should be between 10 and 200 characters")]) 
    submit = SubmitField("Add Comment")
