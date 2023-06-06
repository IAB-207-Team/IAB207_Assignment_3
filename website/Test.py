state_pairs = [Open, Cancelled]

class UpdateEvent(FlaskForm):
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
    ticket_status = SelectField(label='Status', choices=state_pairs)
    submit = SubmitField('Create')
    
@bp.route('/update/<int:event_id>', methods=['GET', 'POST'])
@login_required
def update(event_id):
    print('Method type:', request.method)
    event = Event.query.get_or_404(event_id)
    form = UpdateEvent(obj=event)

    if form.validate_on_submit():
        # Call the function that checks and returns image
        db_file_path = check_upload_file(form)

        # Update the event details with the form data
        event.event_title = form.event_title.data
        event.date = form.date.data
        event.start_time = form.start_time.data
        event.end_time = form.end_time.data
        event.description = form.description.data
        event.genre = form.genre.data
        event.location = form.location.data
        event.amount_of_tickets = form.amount_of_tickets.data
        event.ticket_price = form.ticket_price.data
        event.image = db_file_path
        event.ticket_status = form.ticket_status.data

        # Commit the changes to the database
        db.session.commit()

        print('Successfully updated event details', 'success')
        # Always end with a redirect when form is valid
        return redirect(url_for('auth.create'))

    return render_template('user.html', form=form)
