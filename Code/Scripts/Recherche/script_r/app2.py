# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dbb import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

app.layout = html.Div(children=[
    html.H1(children='Projet Qualité des cours deau Pays de la Loire', style={'textAlign': 'center', 'color' :'black'}),

    html.Div(children='Passage de la Certification data python', style={'textAlign': 'center'}),

    dcc.Graph(
        id='Graph_0',
        figure=fig,
    ),

    dcc.Graph(
        id='Graph_1',
        figure=fig6,
    ),

    dcc.Graph(
        id='Graph_2',
        figure=fig3,
    ),

    dcc.Graph(
        id='Graph_3',
        figure=fig4,
    ),

    dcc.Graph(
        id='Graph_4',
        figure=fig5,
    ),

    dcc.Graph(
        id='Graph_5',
        figure=fig7,
    )


])

if __name__ == '__main__':
    app.run_server(debug=True)