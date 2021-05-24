import dash
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import os
# from data import *

external_stylesheets = 'assets/bulma.min.css'
app = dash.Dash(__name__)

username='postgres'
password=os.environ.get('pg_psw')
port=5432
engine = create_engine(f'postgresql://{username}:{password}@localhost:5432/collection5')


colors = { 
    'text' : '#ff0000',
    'plot_color': '#d3d3d3',
    'paper_color': '#rf0000',
    'background': 'black'
    }

np.random.seed(50)
x_rand = np.random.randint(1,60,60)
y_rand = np.random.randint(1,60,60)

rum = pd.read_sql("""SELECT producteur.nom_producteur as marque, count(produit.nom_produit) as compte
FROM producteur
INNER JOIN origine
on producteur.code_origine = origine.code_origine
INNER JOIN produit
on producteur.code_producteur = produit.code_producteur
WHERE origine.nom = 'Martinique'
GROUP BY producteur.nom_producteur, origine.nom
LIMIT 10;
""", engine)


app.layout = html.Div(
    html.Div(
        className="column is-12 ",
        children=[
            html.Div(
                className="columns",
                children=[
                    html.Div(
                        className="column is-6",
                        children=[
                            html.H1('Demo technique certification développeur DATA',
                                    style={
                                        'textAlign': 'center',
                                        'color': colors['text']
                                    }),

                            dcc.Graph(
                                id='Histo',
                                figure={
                                    'data': [
                                        {'x': rum.marque, 'y': rum.compte, 'type': 'bar', 'name': 'First chart'},
                                    ]}),

                        ]
                    ),
                    html.Div(
                        className="column is-6",
                        children=[

                            html.H1("titre 2",
                                    style={'textAlign': 'center',
                                           'color': 'black',
                                           'margin-bottom': '15px',
                                           'font-size': 'xx-large'}),
                            dcc.Graph(
                                id='scatter_chart',
                                figure={
                                    'data': [
                                        go.Scatter(
                                            x=rum.marque,
                                            y=rum.compte,
                                            mode='markers'
                                        )
                                    ],

                                    'layout': go.Layout(
                                        title='Dispersion producteur',
                                        xaxis={'title': 'producteur'},
                                        yaxis={'title': 'nom'},
                                        hovermode='closest'
                                    )
                                }),
                        ]
                    ),

                ]),

        ])
)


            # html.Button('Submit', id= 'submit form'),

            # html.Br(),
            # html.Br(),

            # html.Label('Choisis une marque'),
            
            # dcc.Dropdown(
            #     id = 'first-dropdown',
            #     options = [
            #         {'label' : 'HSE', 'value': 'hse'},
            #         {'label' : 'Clement', 'value': 'clt'},
            #         {'label' : 'A 1710', 'value': 'A 1'}
            #     ],
            #     #value = 'Martinique',
            #     multi=True,
            #     placeholder = " Select une Marque"

            # ),



            # html.Br(),
            # html.Br(),

            # dcc.Textarea(
            #     placeholder = 'Input your feedback',
            #     value = 'Placeholder for text',
            #     style = {'width': '100%'}
            # )

               



if __name__ == '__main__':
    app.run_server(debug=True)