import os
import sys
sys.path.append(os.path.realpath(os.path.dirname(__file__)))

from bokeh.io import curdoc
from app import BokehServerApp

app = BokehServerApp()

curdoc().add_root(app.get_layout())
