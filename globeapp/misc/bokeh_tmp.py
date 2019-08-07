__author__ = 'volodya'

import bokeh.plotting as bp
from bokeh.embed import components
import datetime

# bp.output_file("line.html")

p = bp.figure(plot_width=400, plot_height=400)

arg = [datetime.datetime.now() + datetime.timedelta(minutes=i*i) for i in range(5)]

p.line(arg, [6, 7, 2, 4, 5], line_width=4, color="green")
p.line(arg, [1, 6, 3, 1, 2], line_width=4, color="darkorange")
p.line(arg, [1, 5, 2, 6, 1], line_width=4, color="teal")
print(p)
bp.show(p)