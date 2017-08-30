from flask import Flask, render_template, request

from bokeh.embed import autoload_server, components
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure
import pandas as pd

flask_app = Flask(__name__)

@flask_app.after_request
def add_header(r):  #this is just to prevent caching of JS code
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


def get_code(obj):
    """Creates html/JS code from Bokeh chart object"""
    js, div = components(obj)
    return js + ' ' + div


def get_bar_chart(part, dimension):
    field = '{}_{}'.format(part, dimension)
    df = pd.read_csv('bundled_data/iris.csv')

    IDX = '__index__'
    df = df.sort_values(by=field, ascending=False)
    df = df.iloc[:15]
    df[IDX] = range(1, len(df) + 1)
    df['color'] = df['species'].apply(lambda x: {
        'setosa': 'blue',
        'versicolor': 'red',
        'virginica': 'green'
    }[x])

    src = ColumnDataSource(df)

    bc = figure(
        plot_width=1000,
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

    return bc


# --- flask routes -----------------------------------------------------------


@flask_app.route('/component')
def get_component():
    payload = request.args.to_dict()

    comp = get_bar_chart(payload['part'], payload['dimension'])

    return get_code(comp)


@flask_app.route('/')
@flask_app.route('/embedded_charts')
def embedded_charts():
    html = render_template('embedded_charts.html')
    return render_template('frame.html', content=html)

@flask_app.route('/embedded_server')
def embedded_server():
    script = autoload_server(model=None, url='https://bokeh-server-app-seed.herokuapp.com/app_serve')
    html = render_template('embedded_server.html', script=script)
    return render_template('frame.html', content=html)


if __name__ == '__main__':
    print('Opening Flask application on http://localhost:5000/')
    flask_app.run(port=5000)  # With debug=True, Flask server will auto-reload when there are code changes

