from bokeh.models import Div, Slider, Select
from bokeh.models.widgets import Button
from bokeh.layouts import layout, widgetbox

from bokeh.server.server import Server
from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application
from tornado.ioloop import IOLoop

import bokeh_helper as bh
import pandas as pd
import numpy as np


# --- constants -----------------------------------------------------------


class BokehApp:
    def update(self):
        # update parameters
        sample_size = self.sample_size_ctrl.value
        width_length = self.width_length_ctrl.value

        # --- Heatmap -----------------------------------------------------------

        df = self.df
        if sample_size < len(df):
            df = df.sample(sample_size)

        sepal = np.array(df['sepal_' + width_length])
        petal = np.array(df['petal_' + width_length])
        A = np.repeat(sepal, sample_size).reshape(sample_size, sample_size)
        B = np.repeat(petal, sample_size).reshape(sample_size, sample_size)
        M = A/B
        hm_df = bh.get_heatmap_df(df, M)
        hm = bh.get_heatmap(hm_df, 'id_x', 'id_y')
        self.heatmap_div.text = bh.get_code(hm)


    def __init__(self):
        self.df = pd.read_csv('bundled_data/iris.csv')
        self.df.index = pd.Series(data=range(len(self.df)), name='id')

        # div holding the chart
        self.heatmap_div = Div(text='')
        self.bar_chart_div = Div(text='')

        # controls
        self.sample_size_ctrl = Slider(title="Number of bars", value=10, start=5, end=20, step=1)
        self.width_length_ctrl = Select(title="Width of length?", options=['width', 'length'], value='width')

        self.submit_btn = Button(label="Submit", button_type="success")
        self.submit_btn.on_click(self.update)

        self.update()

    def get_layout(self):
        sizing_mode = 'fixed'

        inputs = widgetbox(
            [
                self.submit_btn,
                Div(text='<hr>'),

                Div(text='<b>Section A</i>'),
                self.width_length_ctrl,
                self.sample_size_ctrl,
            ],
            sizing_mode=sizing_mode, responsive=True
        )

        charts = layout([
            [Div(text='<h2>Heatmap</h2>', width=500)],
            [self.heatmap_div],

            [Div(text='<h2>Bar chart</h2>', width=500)],
            [self.bar_chart_div],
        ])

        l = layout([
            [inputs, charts],
            [Div(height=200)]  # some empty space
        ], sizing_mode=sizing_mode)

        return l


def run_app(show=True):
    def modify_doc(doc):
        app = BokehApp()

        l = app.get_layout()
        doc.add_root(l)
        doc.title = 'Some dashboard title'

    io_loop = IOLoop.current()

    bokeh_app = Application(FunctionHandler(modify_doc))

    server = Server({'/': bokeh_app}, io_loop=io_loop, allow_websocket_origin=["*"], host='*', address='0.0.0.0')
    server.start()

    print('Starting Bokeh application on http://localhost:5006/')

    if show:
        io_loop.add_callback(server.show, "/")
    io_loop.start()


if __name__ == '__main__':
    run_app()
