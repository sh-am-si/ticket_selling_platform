__author__ = 'volodya'

from globeapp import db
from globeapp.models import Play, Ticket

for t in Play.query.all():
    print(t.id ,t)

print(Play.query.get(1))

for t in Ticket.query.all():
    print(t)