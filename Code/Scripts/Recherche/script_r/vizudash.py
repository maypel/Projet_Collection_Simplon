#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import pandas as pd 
import psycopg2
#import folium
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
conn = psycopg2.connect(
        user = "postgres",
        password = os.environ.get("pg_psw"),
        host = "localhost",
        port = "5432",
        database = "collection5"
)
cur = conn.cursor()
cur.execute("""SELECT origine.nom, count(produit.nom_produit)
FROM origine
INNER JOIN producteur
ON origine.code_origine = producteur.code_origine 
INNER JOIN produit
ON producteur.code_producteur = produit.code_producteur
group by origine.nom
order by count(produit.nom_produit) DESC
;
""")
requete = cur.fetchall()

dataf = pd.DataFrame(requete)
dataf.columns = ['nom', 'compte']

fig = px.sunburst(dataf, path=["nom", "compte"], color="nom",
           hover_data=dataf.columns,
           values="compte")

fig2 = px.choropleth(dataf, locations="nom",
                            locationmode="country names",
                            color="nom",
                            hover_name="compte",
                            projection='mollweide',
                            title='Production',
                            color_continuous_scale=px.colors.sequential.Plasma)

cur.execute("""SELECT producteur.nom_producteur, origine.nom, count(produit.nom_produit)
FROM producteur
INNER JOIN origine
ON producteur.code_origine = origine.code_origine 
INNER JOIN produit
ON producteur.code_producteur = produit.code_producteur
group by producteur.nom_producteur, origine.nom
order by count(produit.nom_produit) DESC
Limit 10
;
""")
requete2 = cur.fetchall()         
dfproducteur = pd.DataFrame(requete2)
dfproducteur.columns = ['producteur', 'origine', 'compte']


fig3=px.histogram(dfproducteur,
             x="producteur", 
             y="compte", 
             color='origine'
           )


fig4=px.sunburst(dfproducteur, path=["origine", "producteur"], color="compte",
           hover_data=dfproducteur.columns,
           values="compte")





app.layout = html.Div(children=[
    html.H1(children='Collect spirit'),

    html.Div(children='''
        Let's Rhum
    '''),

    dcc.Graph(
        id='graph1',
        figure=fig
        
    ),

     dcc.Graph(
        id='graph2',
        figure=fig2
        
    ),

    dcc.Graph(
        id='Graph_3',
        figure=fig3
    ),

    dcc.Graph(
        id='Graph_4',
        figure=fig4
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)