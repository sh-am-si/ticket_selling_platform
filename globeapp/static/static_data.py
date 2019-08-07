__author__ = 'volodya'

import datetime
# from datetime import timedelta
# from datetime import datetime
import collections

'''
key : id
value[0]: name
value[1]: price multiplier
up to now 3 fields 
'''
# TODO consider whether there is a reason to make an orbitrary number of fields

ticket_category_dict = {0: ('ordinary', 1.),
                        1: ('premium', 1.2),
                        2: ('vip', 1.4),
                        }

reservation_time = datetime.timedelta(minutes=15)
default_past_date = datetime.datetime(year=1900, month=1, day=1, hour=0, minute=0)

date_output_template = "%a, %-d %b %Y, %H:%M"

TicketInfo = collections.namedtuple('TicketInfo',
                                    ['name', 'play', 'status', 'email', 'price', 'row', 'seat', 'category'])
