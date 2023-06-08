from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, DateField, TimeField, IntegerField, DecimalField, SelectField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed

#List of allowed files when creating an event
ALLOWED_FILE = {'PNG','JPG','png','jpg'}

#Create new event
class CreateEvent(FlaskForm):
    event_title = StringField('Event Title', validators=[InputRequired()])
    date = DateField('Start Date', format='%Y-%m-%d')
    start_time = TimeField('Start Time')
    end_time = TimeField('End Time')
    description = TextAreaField('Description', validators=[InputRequired()])
    genre = StringField('Genre')
    location = TextAreaField('Mailing Address', validators=[InputRequired()])
    amount_of_tickets = IntegerField('Amount')
    ticket_price =IntegerField('Price', render_kw={'TIcket Price': 'Enter the ticket price'})
    image = FileField('Destination Image', validators=[FileRequired(message='Image cannot be empty'), FileAllowed(ALLOWED_FILE, message='Only supports png,jpg,JPG,PNG')])
    submit = SubmitField('Create')

# Booking an event form 
class BookEvent(FlaskForm):
    email_id=StringField("Email Address", validators=[InputRequired('Enter email')])
    card_no = IntegerField('Card Number' , validators=[InputRequired(), Length(min=0, max=16)])
    quantity = IntegerField('Quantity')
    expiry = StringField('Expiry Date')
    CVV =  IntegerField('Security Code')
 

#creates the login information
class LoginForm(FlaskForm):
    email_id=StringField("User Name", validators=[InputRequired('Enter User Name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

#Allows for a user to create an account
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(), EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    submit = SubmitField("Register")

# Allows for the user to add a comment to an event
class CommentForm(FlaskForm):
    text = TextAreaField("Comment", validators=[InputRequired(), Length(min=1, max=200, message="Comment should be between 10 and 200 characters")]) 
    submit = SubmitField("Add Comment")
    
# Flask forn to update an events information
class UpdateEvent(FlaskForm):
    state_pairs = ['Open', 'Cancelled'] # created a list of options for a user to choose when upating the status of the event
    event_title = StringField('Event Title', validators=[InputRequired()])
    date = DateField('Start Date', format='%Y-%m-%d')
    start_time = TimeField('Start Time')
    end_time = TimeField('End Time')
    description = TextAreaField('Description', validators=[InputRequired()])
    genre = StringField('Genre')
    location = TextAreaField('Mailing Address')
    amount_of_tickets = IntegerField('Amount')
    ticket_price =IntegerField('Price', render_kw={'TIcket Price': 'Enter the ticket price'})
    ticket_status = SelectField(label='Status', choices=state_pairs)
    submit = SubmitField('Create')
