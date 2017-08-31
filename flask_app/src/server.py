from flask import Flask, render_template, request
from bokeh.embed import autoload_server, components
from common import sample_bokeh_chart

flask_app = Flask(__name__)

@flask_app.after_request
def add_header(r):
    """this is just to prevent caching of JS code"""
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


# --- flask routes -----------------------------------------------------------


@flask_app.route('/bar-chart')
def get_bar_chart_code():
    """route to get the HTML/JS code of a bar chart"""
    payload = request.args.to_dict()

    bc = sample_bokeh_chart.get_bar_chart(payload['part'], payload['dimension'], int(payload['nresults']))
    js, div = components(bc)

    return js + ' ' + div


@flask_app.route('/')
@flask_app.route('/embedded-charts')
def embedded_charts():
    """route to demonstrate embedding bokeh charts"""
    html = render_template('embedded_charts.html')
    return render_template('frame.html', content=html)


@flask_app.route('/embedded-server')
def embedded_server():
    """route to demonstrate embedding whole bokeh server app"""
    script = autoload_server(model=None, url='https://bokeh-server-app-seed.herokuapp.com/serve_app')  # change this to point to your app
    html = render_template('embedded_server.html', script=script)
    return render_template('frame.html', content=html)


if __name__ == '__main__':
    print('Opening Flask application on http://localhost:5000/')
    flask_app.run(port=5000)

