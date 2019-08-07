__author__ = 'volodya'

'''
row_num, seat_num = 300, 500 
objects sizes for dtype=np.uint8 
                    np.iinfo(np.uint8)
                    iinfo(min=0, max=255, dtype=uint8)
list of namedtuples 1320848
np array 450112
pandas dataframe 450104

objects sizes for dtype=np.uint16 
                    np.iinfo(np.uint16)
                    iinfo(min=0, max=65535, dtype=uint16)
                    
list of namedtuples 1320848
np array 450112
pandas dataframe 450104
list of namedtuples 1320848
np array 900112
pandas dataframe 900104

'''

from collections import namedtuple
import numpy as np
import pandas as pd
import sys
from globeapp.static.static_data import ticket_category_dict

from datetime import datetime

row_num, seat_num = 80, 80  # the hall shouldn't be rectangular

TicketType = namedtuple('TicketType', ['row', 'seat', 'category'])

if __name__ == '__main__':
    nt_list = []
    categories = np.array(list(ticket_category_dict.keys()))
    print(categories, categories.shape, type(categories), categories.ndim)
    np_array = np.zeros(shape=(row_num * seat_num, 3), dtype=np.uint8)
    t1 = datetime.now()
    for r in range(1, row_num + 1):
        for s in range(1, seat_num + 1):
            nt_list.append(TicketType(row=r, seat=s, category=np.random.choice(categories)))
    delta1 = datetime.now() - t1

    t1 = datetime.now()
    np_array[:, 0] = np.arange(1, row_num + 1).repeat(seat_num)  # filling up rows
    np_array[:, 1] = np.tile(np.arange(1, seat_num + 1), row_num)  # filling up seats
    np_array[:, 2] = np.random.choice(categories, size=row_num * seat_num)  # filling up category
    # it might be also some specified function
    # Don't think it is more efficient than a loop nevertheless up to now it might look like this also
    # update. it happened to do it 100x quicker
    delta2 = datetime.now() - t1
    df = pd.DataFrame({'rows': np_array[:, 0],
                       'seats': np_array[:, 1],
                       'category': np_array[:, 2]})

    # for t in range(len(nt_list)):
    #     print(nt_list[t], np_array[t,:], df.iloc[t,:])

    print('list of namedtuples', sys.getsizeof(nt_list), delta1)
    print('np array', sys.getsizeof(np_array), delta2)
    print('pandas dataframe', sys.getsizeof(df))
