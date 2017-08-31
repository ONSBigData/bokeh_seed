from flask import Flask, render_template, request

from bokeh.embed import autoload_server, components
from common import sample_bokeh_chart

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


# --- flask routes -----------------------------------------------------------


@flask_app.route('/component')
def get_component():
    payload = request.args.to_dict()

    comp = sample_bokeh_chart.get_bar_chart(payload['part'], payload['dimension'], payload['nresults'])

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

