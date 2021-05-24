#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
from sqlalchemy import create_engine
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html

import dash_table
import os

app = dash.Dash(__name__)

username='postgres'
password=os.environ.get('pg_psw')
port=5432
engine = create_engine(f'postgresql://{username}:{password}@localhost:5432/collection5')


colors = {
    'background': 'yellow',
    'text': 'red'
}
#set the page size
PAGE_SIZE = 10

df1 = pd.read_sql("""Select producteur.nom_producteur, count(produit.nom_produit)
from producteur
inner join origine
on producteur.code_origine = origine.code_origine
inner join produit
on producteur.code_producteur = produit.code_producteur
where origine.nom = 'Martinique'
group by producteur.nom_producteur, origine.nom;
""", engine)

app.layout = html.Div(children=[
    
    html.H1(children='Projet de collection de spiritueux', style={'textAlign': 'center', 'color': 'red'}),

    html.H2(children='Let\'s rhum', style={'textAlign': 'center', 'color': 'orange'}),

    html.Iframe(
        id='Map',
        srcDoc= open('Producteur_martinique.html', 'r').read(), width='60%', height='20%'
    ),


    dcc.Graph(
        id='Histo',
        figure=fig2
    ),
    
    dcc.Graph(
        id='Camembert',
       figure=fig3
     ),

    html.P("Subplots Width:"),

    dcc.Slider(
        id='slider-width', min=0, max=1, 
        value=0.5, step=0.01),
    

    
    dash_table.DataTable(
        id='table-sorting-filtering',
        style_data={
        'whiteSpace': 'normal',
        'height': 'auto'
        },
        style_table={
            'maxHeight': '200px'
            ,'overflowY': 'scroll'
        },
        columns=[
            {'name': i, 'id': i} for i in df1.columns
        ],
        page_current= 0,
        page_size= PAGE_SIZE,
        page_action='custom',
        filter_action='custom',
        filter_query='',
        sort_action='custom',
        sort_mode='multi',
        sort_by=[]
        )
    
]
)

if __name__ == '__main__':
    app.run_server(debug=True)