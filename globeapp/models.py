from datetime import datetime
from globeapp import db
from globeapp.static.static_data import ticket_category_dict
from globeapp.static.static_data import date_output_template
from globeapp.static.static_data import default_past_date, reservation_time


class Play(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(20), unique=False, nullable=False)
    title = db.Column(db.String(20), unique=False, nullable=False)
    date = db.Column(db.DateTime, index=True, nullable=False)
    venue = db.Column(db.String(120), unique=False, nullable=True) # Todo is not used

    price = db.Column(db.Float, nullable=False, default=20.)

    tickets = db.relationship('Ticket', backref='concert', lazy=True)

    def __repr__(self):
        return f'{self.author} : {self.title} at {self.date.strftime(date_output_template)}'

    def has_available_tickets(self):
        return bool(self.get_available_tickets())

    def get_available_tickets(self):
         return Ticket.query.filter(Ticket.play_id == self.id,
                                   Ticket.booked < datetime.now() - reservation_time,
                                   Ticket.bought == False).all()


class Ticket(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), unique=False, nullable=True)
    last_name = db.Column(db.String(30), unique=False, nullable=True)
    email = db.Column(db.String(120), unique=False, nullable=True)
    play_id = db.Column(db.Integer, db.ForeignKey('play.id'), nullable=False)
    bought = db.Column(db.Boolean, default=False)
    booked = db.Column(db.DateTime, default=default_past_date)
    row = db.Column(db.Integer, default=0)
    seat = db.Column(db.Integer, default=0)
    category = db.Column(db.Integer, default=0)  # TODO
    secret_code = db.Column(db.String(16))  # should I put unique=True?

    def get_price(self):
        return Play.query.get(self.play_id).price * ticket_category_dict[self.category][1]

    def __repr__(self):
        # EUR symbol : +u'\u20AC'
        return f'{self.id} {ticket_category_dict[self.category][0]} ticket, row {self.row}, seat {self.seat}: {self.get_price()}\u20AC'
