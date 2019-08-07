__author__ = 'volodya'

'''
temporary file
'''

import socket, errno

# Port check
# https://stackoverflow.com/questions/2470971/fast-way-to-test-if-a-port-is-in-use-using-python
# modified default port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind(("127.0.0.1", 5000))
except socket.error as e:
    if e.errno == errno.EADDRINUSE:
        print("Port is already in use")
    else:
        # something else raised the socket.error exception
        print(e)

s.close()

from globeapp.models import Play, Ticket
from datetime import datetime
import numpy as np
from globeapp import db
from globeapp.misc.init_ticket_allocation import init_array

db.drop_all()
db.create_all()


def set_tickets_4play(_play, rows=4, seats=6):

    array = init_array(row_num=rows,
                       seat_num=seats)

    for i in range(array.shape[0]):

        #
        # OMG, SQLALCHEMY doesn't convert types!!!!
        #
        ticket = Ticket(first_name='',
                        last_name='',
                        email='',
                        play_id=_play.id,
                        row=int(array[i, 0]),
                        seat=int(array[i, 1]),
                        category=int(array[i, 2]))
        _play.tickets.append(ticket)
    db.session.commit()


available_days = set(range(1, 32))

for day in np.random.choice(list(available_days), 2, replace=False):
    available_days.remove(day)
    current_play = Play(author='W. Shakespeare',
                        title='Macbeth',
                        date=datetime(year=2019, month=10, day=day, hour=19),
                        price=np.random.choice(np.arange(20, 50, 10)))
    db.session.add(current_play)
    db.session.commit()
    set_tickets_4play(current_play, 10,20)

for day in np.random.choice(list(available_days), 3, replace=False):
    available_days.remove(day)
    current_play = Play(author='W. Shakespeare',
                        title='Midsummer Night\'s Dream',
                        date=datetime(year=2019, month=10, day=day, hour=17),
                        price=np.random.choice(np.arange(20, 50, 10)))
    db.session.add(current_play)
    db.session.commit()
    set_tickets_4play(current_play, 30, 40)

for day in np.random.choice(list(available_days), 3, replace=False):
    current_play = Play(author='W. Shakespeare',
                        title='Richard III',
                        date=datetime(year=2019, month=10, day=day, hour=18),
                        price=np.random.choice(np.arange(20, 50, 10)))
    db.session.add(current_play)
    db.session.commit()
    set_tickets_4play(current_play, 20, 10)


print('PLAYS')

for i, current_play in enumerate(Play.query.order_by(Play.date).all()):
    print(current_play.id, current_play)

print('TICKETS')

for i, ticket in enumerate(Ticket.query.order_by(Ticket.first_name).all()):
    print(ticket.id, ticket, Play.query.get(ticket.play_id))

# print(Play.query.get(1).date, dir(Play.query.get(1).date))
# date = Play.query.get(1).date
# print(date)
# print(date.strftime('%a, %d %b %Y, %H:%M'))
