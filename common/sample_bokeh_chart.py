from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure
import pandas as pd
import os


def get_bar_chart(part, dimension, nresults):
    field = '{}_{}'.format(part, dimension)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    df = pd.read_csv(dir_path + '/bundled_data/iris.csv')

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