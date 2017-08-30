from bokeh.models import Div, Slider, Select, Button, ColumnDataSource, HoverTool
from bokeh.layouts import layout, widgetbox
from bokeh.plotting import figure
from bokeh.embed import components

from bokeh.server.server import Server
from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application
from tornado.ioloop import IOLoop

import pandas as pd
import sys

# --- constants -----------------------------------------------------------

APP_TITLE = 'Bokeh server seed app'

PAGE_WIDTH = 1300
WIDGET_BOX_WIDTH = 250
CHARTS_WIDTH = PAGE_WIDTH - WIDGET_BOX_WIDTH
DIV_WIDTH = CHARTS_WIDTH // 2 - 20


class BokehServerApp:
    def update(self):
        nresults = self.nresults_ctrl.value
        dimension = self.dimension_ctrl.value
        part = self.part_ctrl.value

        field = '{}_{}'.format(part, dimension)

        df = self.base_df.copy()
        IDX = '__index__'
        df = df.sort_values(by=field, ascending=False)
        df = df.iloc[:nresults]
        df[IDX] = range(1, len(df) + 1)
        df['color'] = df['species'].apply(lambda x: {
            'setosa': 'blue',
            'versicolor': 'red',
            'virginica': 'green'
        }[x])

        src = ColumnDataSource(df)

        bc = figure(
            plot_width=CHARTS_WIDTH,
            title='{} {}'.format(part, dimension),
            tools=[HoverTool(tooltips=[(c, '@{}'.format(c)) for c in df.columns])]
        )

        bc.vbar(
            top=field,
            bottom=0,
            x=IDX,
            width=0.5,
            color='color',
            source=src
        )

        bc.xaxis[0].ticker.desired_num_ticks = len(df)
        bc.yaxis.axis_label = '{} {}'.format(part, dimension)
        bc.xaxis.axis_label = 'index'

        js, div = components(bc)
        self.chart_div.text = js + ' ' + div

    def __init__(self):
        self.base_df = pd.read_csv('./bundled_data/iris.csv')

        self.top_div = Div(text='', width=CHARTS_WIDTH)

        self.chart_div = Div(text='', width=CHARTS_WIDTH)

        self.nresults_ctrl = Slider(title="Number of results", value=10, start=10, end=30, step=1)
        self.dimension_ctrl = Select(title="Dimension", options=['width', 'length'], value='width')
        self.part_ctrl = Select(title="Part", options=['sepal', 'petal'], value='sepal')

        self.submit_btn = Button(label="Update", button_type="success")
        self.submit_btn.on_click(self.update)

        self.update()

    def get_layout(self):
        sizing_mode = 'fixed'

        inputs_column = widgetbox(
            [
                self.submit_btn,
                Div(text='<hr>'),

                self.nresults_ctrl,
                self.part_ctrl,
                self.dimension_ctrl
            ],
            sizing_mode=sizing_mode, responsive=True, width=WIDGET_BOX_WIDTH
        )

        main_column = layout([
            [self.top_div],
            [self.chart_div]
        ])

        l = layout([
            [inputs_column, main_column],
            [Div(height=200)]  # some empty space
        ], sizing_mode=sizing_mode)

        return l


def run_app(show=True):
    def modify_doc(doc):
        app = BokehServerApp()
        l = app.get_layout()
        doc.add_root(l)
        doc.title = APP_TITLE

    io_loop = IOLoop.instance()
    bokeh_app = Application(FunctionHandler(modify_doc))

    server = Server(
        {'/': bokeh_app},
        io_loop=io_loop,
        allow_websocket_origin=["*"],
        address='localhost',
        use_xheaders=True
    )
    server.start()

    print('Starting Bokeh ioloop. Url: http://localhost:5006/')
    sys.stdout.flush()

    if show:
        io_loop.add_callback(server.show, "/")

    io_loop.start()


if __name__ == '__main__':
    run_app()
