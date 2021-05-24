import dash
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import os
# from data import *

app = dash.Dash(__name__)

username='postgres'
password=os.environ.get('pg_psw')
port=5432
engine = create_engine(f'postgresql://{username}:{password}@localhost:5432/collection5')


# colors = { 
#     'text' : '#ff0000',
#     'plot_color': '#d3d3d3',
#     'paper_color': '#rf0000',
#     'background': 'black'
#     }


import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output

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

rum = pd.read_sql("""Select producteur.nom_producteur as marque, count(produit.nom_produit) as compte
from producteur
inner join origine
on producteur.code_origine = origine.code_origine
inner join produit
on producteur.code_producteur = produit.code_producteur
where origine.nom = 'Martinique'
group by producteur.nom_producteur, origine.nom;
""", engine)

app.layout = html.Div(
    children=[
        html.Div(className='column is-12',
                 children=[
                    html.Div(className='four columns div-user-controls',
                             children=[
                                 html.H2('Inventaire Collection'),
                                 html.P('Visualising time series with Plotly - Dash.'),
                                 html.P('Pick one or more stocks from the dropdown below.'),
                                 html.Div(
                                     className='div-for-dropdown',
                                     children=[
                                         dcc.Dropdown(
                                                    id = 'first-dropdown',
                                                    options = [
                                                        {'label' : 'HSE', 'value': 'hse'},
                                                        {'label' : 'Clement', 'value': 'clt'},
                                                        {'label' : 'A 1710', 'value': 'A 1'}
                                                    ],
                                                    #value = 'Martinique',
                                                    multi=True,
                                                    placeholder = " Select une Marque"

                                                )
                                     ],
                                     style={'color': '#1E1E1E'})
                                ]
                             ),
                    html.Div(className='eight columns div-for-charts bg-grey',
                             children=[
                                 dcc.Graph(
                            id = 'Histo',
                            figure = {
                                'data' : [
                                    { 'x' : rum.marque, 'y':rum.compte, 'type': 'bar', 'name': 'First chart'},
                                    ]
                                
                            }
                        )
                             ])
                              ])
        ]

)



if __name__ == '__main__':
    app.run_server(port = 4050,debug=True)