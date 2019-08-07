__author__ = 'volodya'

import numpy as np
from globeapp.static.static_data import ticket_category_dict

def init_array(row_num, seat_num):

    categories = np.array(list(ticket_category_dict.keys()))
    array = np.zeros(shape=(row_num * seat_num, 3), dtype=np.uint8)
    array[:, 0] = np.arange(1, row_num + 1).repeat(seat_num)  # filling up rows
    array[:, 1] = np.tile(np.arange(1, seat_num + 1), row_num)  # filling up seats
    array[:, 2] = np.random.choice(categories, size=row_num * seat_num)  # filling up category

    return array
