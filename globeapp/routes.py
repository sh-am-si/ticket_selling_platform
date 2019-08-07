
from flask import render_template
from flask import url_for
from flask import flash
from flask import redirect
from flask import session
from flask import jsonify
from flask import request

import bokeh.plotting as bp
from bokeh.embed import components
from bokeh.resources import INLINE

import stripe
import secrets

from globeapp import app
from globeapp.forms import HomeForm
from globeapp.forms import StatsForm
from globeapp.models import Play, Ticket
from datetime import datetime
from globeapp import db
from globeapp.static.static_data import ticket_category_dict
from globeapp.static.static_data import reservation_time
from globeapp.static.static_data import default_past_date
from globeapp.static.static_data import TicketInfo

import globeapp


def update_selected_fields(form):


    form.play_select.choices = []
    for play in Play.query.order_by(Play.date).all():
        if play.has_available_tickets():
            form.play_select.choices.append((play.id, play))

    if form.play_select.data is not None:
        play_id = form.play_select.data
    else:
        play_id = 1
    if form.play_select.choices:

        form.ticket_select.choices = [(ticket.id, str(ticket)) for ticket in
                                      Play.query.get(play_id).get_available_tickets()]


@app.before_first_request
def initial():
    session.clear()
    session['ticket_list'] = []
    session['price'] = 0


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = HomeForm(request.form)

    update_selected_fields(form)

    if 'ticket_list' not in session:
        session['ticket_list'] = []

    if 'price' not in session:
        session['price'] = 0

    if request.method == 'POST' and form.validate_on_submit():
        try:
            ticket_id = form.ticket_select.data
            if ticket_id not in session['ticket_list']:
                ticket = Ticket.query.get(ticket_id)
                ticket.first_name = form.first_name.data
                ticket.last_name = form.last_name.data
                ticket.email = form.email.data
                ticket.booked = datetime.now()
                ticket.play_id = form.play_select.data
                session['price'] += ticket.get_price()
                session['ticket_list'].append(ticket_id)  # the same part of awkward solution

                flash('your ticket was added')
                db.session.commit()
        except:
            flash('your ticket was not added', 'alarm')

    ticket_list = [Ticket.query.get(t) for t in session['ticket_list']]
    ticket_list.sort(key=lambda x: Play.query.get(x.play_id).date)

    return render_template('home.html',
                           form=form,
                           ticket_list=[(str(ticket),
                                         str(Play.query.get(ticket.play_id))) for ticket in ticket_list],
                           price=session['price'])


@app.route("/cancel")
def cancel():
    if 'price' in session:
        session['price'] = 0.

    if 'ticket_list' in session:
        for t in session['ticket_list']:
            Ticket.query.get(t).booked = default_past_date

    db.session.commit()
    session.clear()
    return redirect(url_for('home'))


@app.route("/purchase")
def purchase():
    ticket_list = [Ticket.query.get(t) for t in session['ticket_list']]
    ticket_list.sort(key=lambda x: Play.query.get(x.play_id).date)
    image_path = '/static/logo.png'

    return render_template('purchase.html',
                           key=globeapp.STRIPE_PUBLISHABLE_KEY,
                           ticket_list=[(str(ticket),
                                         str(Play.query.get(ticket.play_id))) for ticket in ticket_list],
                           num=len(ticket_list),
                           image_path=image_path,
                           price=session['price'])


@app.route('/pay', methods=['POST'])
def pay():
    customer = stripe.Customer.create(email=request.form['stripeEmail'],
                                      source=request.form['stripeToken'])

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=int(session['price'] * 100),
        currency='EUR',
        description='The Product'
    )

    bought_tickets = []
    if charge['status'] == 'succeeded':
        for t in session['ticket_list']:
            ticket = Ticket.query.get(t)
            ticket.bought = True
            ticket.secret_code = secrets.token_hex(16)
            bought_tickets.append(TicketInfo(name=ticket.first_name + ' ' + ticket.last_name,
                                             play=Play.query.get(ticket.play_id),
                                             status=True,
                                             email=ticket.email,
                                             price=ticket.get_price(),
                                             row=ticket.row,
                                             seat=ticket.seat,
                                             category=ticket_category_dict[ticket.category]))

    return render_template('thanks.html',
                           bought_tickets=bought_tickets)


@app.route('/stats', methods=['GET', 'POST'])
def stats():
    form = StatsForm(request.form)
    # form.play_select.choices = [(0, 'All')]
    for play in Play.query.order_by(Play.date).all():
        if play.has_available_tickets():
            form.play_select.choices.append((play.id, play))

    if request.method == 'POST' and form.validate():
        # play_id = form.play_select.data
        # if play_id == 0:
        #     tickets = Ticket.query.order_by(Ticket.booked)
        # else:

        tickets = Ticket.query.filter(Ticket.play_id == play_id).order_by(Ticket.booked)

        query = tickets.filter(Ticket.booked > reservation_time)
        first = query.first()
        date = first.booked
        arg = [date]
        booked = [1]
        while len(query.all()):
            query = tickets.filter(Ticket.booked > date)
            first = query.first()
            if first:
                date = first.booked
                arg.append(date)
                booked.append(booked[-1] + 1)

        p = bp.figure(plot_width=800, plot_height=400)
        p.line(arg, booked, line_width=4, color="green")

        script, div = components(p)

        return render_template('stats.html',
                           form=form,
                           plot_script=script,
                           plot_div=div,
                           resources=INLINE.render()
                           )
    else:
        return render_template('stats.html',
                           form=form,
                           plot_script='',
                           plot_div='',
                           resources=''
                           )


@app.route('/ticket/<int:play_id>/<int:current_ticket>')
def tickets(play_id, current_ticket):
    ticket_array = []

    for ticket in Play.query.get(play_id).get_available_tickets():
        ticketObj = {}
        if ticket.id not in session['ticket_list'] and ticket.id != current_ticket:
            # awkward solution ... :(
            ticketObj['id'] = ticket.id
            ticketObj['name'] = str(ticket)
            ticket_array.append(ticketObj)

    return jsonify({'tickets': ticket_array})
