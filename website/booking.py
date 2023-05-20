#This is just something I quickly made up, but I might be useful for getting the ticketing system to work
from flask import Flask, render_template, request
import sqlite3

@app.route('/events/<event_id>/book', methods=['GET', 'POST'])
def book_event(event_id):
    cursor.execute('SELECT * FROM events WHERE id = ?', (event_id,))
    event = cursor.fetchone()

    if event is None:
        return 'Event not found', 404

    if request.method == 'POST':
        if event == 0:
            cursor.execute('UPDATE events SET status = ? WHERE id = ?', ('Sold Out', event_id))
            conn.commit()
            return 'Event is sold out'

        new_ticket_count = event - 1
        cursor.execute('UPDATE events SET ticket_count = ? WHERE id = ?', (new_ticket_count, event_id))
        if new_ticket_count == 0:
            cursor.execute('UPDATE events SET status = ? WHERE id = ?', ('Sold Out', event_id))
        conn.commit()

        return 'Ticket booked successfully'

    return render_template('book_event.html', event=event)
