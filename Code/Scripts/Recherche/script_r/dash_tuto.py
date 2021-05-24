from pandas._config.config import options
import dash
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import os

app = dash.Dash()

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



app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
        html.H1(children ='Demo technique certification développeur DATA',
                style = {
                    'textAlign': 'center',
                    'color': colors['text'],
                }),

        html.Div(children ='Inventaire Collection',
                style = {
                    'textAlign': 'center',
                    'color': '#ff0000'
                }),

        dcc.Graph(
            id = 'Histo',
            figure = {
                'data' : [
                    { 'x' : rum.marque, 'y':rum.compte, 'type': 'bar', 'name': 'First chart'},
                     ],
                'layout' : {
                    'title': 'Producteurs les plus présent',
                    'plot_bgcolor': colors['background'],
                    'paper_bgcolor': colors['background'],
                    'font' :{
                        'color': '#237cbf'
                    }

                }
            }
        ),

        dcc.Graph(
            id = 'scatter_chart',
            figure = {
                'data' : [
                    go.Scatter(
                        x = rum.marque,
                        y = rum.compte,
                        mode = 'markers'
                    )                        
                ],

                'layout' : go.Layout(
                    title = 'Dispersion producteur',
                    xaxis = { 'title': 'producteur'},
                    yaxis = { 'title': 'nom'},
                    hovermode='closest',
                    plot_bgcolor = colors['background'],
                    paper_bgcolor = colors['background'],
                    
                )
                
            }

        ),

    html.Button('Submit', id= 'submit form'),

        html.Br(),
    html.Br(),

    html.Label('Choisis une marque'),
    
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

    ),

    html.Br(),
    html.Br(),

    html.Label('Slider'),
    dcc.Slider(
        min = 1,
        max = 11,
        value = 5,
        step = .5,
        marks = {i: i for i in range(10)}
    ),
    
    html.Br(),
    html.Br(),

    html.Label('Range Slider'),
    dcc.RangeSlider(
        min = 1,
        max = 11,
        value = [3,7],
        step = .5,
        marks = {i: i for i in range(10)}
    ),

    html.Br(),
    html.Br(),

    html.Div([
    html.Label('Commentaire'),
    dcc.Input(
        placeholder = 'Input your name',
        value = ""
    )
     
    ]),

    html.Br(),
    html.Br(),

    dcc.Textarea(
        placeholder = 'Input your feedback',
        value = 'Placeholder for text',
        style = {'width': '100%'}
    )
])

if __name__ == '__main__':
    app.run_server(port = 4050, debug=True)



    