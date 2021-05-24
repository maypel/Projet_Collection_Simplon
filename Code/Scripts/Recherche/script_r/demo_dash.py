import dash
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from sqlalchemy import create_engine
import os
import plotly.express as px


external_stylesheets = 'assets/bulma.min.css'

app = dash.Dash(__name__)



username='postgres'
password=os.environ.get('pg_psw')
port=5432
engine = create_engine(f'postgresql://{username}:{password}@localhost:5432/collection5')


colors = { 
    'text' : 'white',
    'plot_color': '#d3d3d3',
    'paper_color': '#rf0000',
    'background': 'black'
    }


rum = pd.read_sql("""SELECT producteur.nom_producteur as marque, count(produit.nom_produit) as compte, origine.nom as pays
                        FROM producteur
                        INNER JOIN origine
                        on producteur.code_origine = origine.code_origine
                        INNER JOIN produit
                        on producteur.code_producteur = produit.code_producteur
                        GROUP BY marque, pays
                        ORDER BY compte DESC
                        LIMIT 10;""", engine)

origines = pd.read_sql("""SELECT origine.nom as pays, count(produit.nom_produit) as compte
                        FROM origine
                        INNER JOIN producteur
                        ON origine.code_origine = producteur.code_origine 
                        INNER JOIN produit
                        ON producteur.code_producteur = produit.code_producteur
                        group by origine.nom
                        order by count(produit.nom_produit) DESC
                        Limit 20
                        ;
                        """, engine)

types = pd.read_sql("""SELECT produit.type_rhum as variete, count(produit.type_rhum) as compte, origine.nom as pays
                        FROM produit
                        INNER JOIN producteur
                        ON produit.code_producteur = producteur.code_producteur
                        INNER JOIN origine
                        ON producteur.code_origine = origine.code_origine
                        WHERE (origine.nom = 'Martinique' or origine.nom = 'Guadeloupe') and type_rhum <> 'NaN'and type_rhum <> 'Overproof'
                        GROUP BY variete, pays
                        ORDER BY pays;
                        """, engine)

# rgba(black, 0.5)
app.layout = html.Div(style={'background-image': 'url(https://www.archipel-des-sciences.org/wp-content/uploads/2015/02/canne-a-sucre.jpg)'},
                    children = [

                html.Div(children= [
                    html.H1('Demo technique certification développeur DATA',
                        style = {
                            'textAlign': 'center',
                            'color': colors['text'],
                             'font-weight' : 'bold',
                            'margin-bottom': '35px',
                            'font-size': 'xx-large',
                            'background-color': 'black',
                            'background-repeat': 'no-repeat',
                            'background-position': 'center',
                            'background-size': '100%'
                        })
                ]),

                html.Br(),
                

                html.Div(
        className="column is-12 ",
        children=[
            html.Div(
                className="columns",
                children=[
                    html.Div(
                        className="column is-6",
                        children=[
                            html.H2('Les marques les plus présentes',
                                    style={
                                        'textAlign': 'center',
                                        'color': colors['text']
                                    }),

                            dcc.Graph(
                                id='Histo',
                                figure=px.histogram(types, 
                                                    x="variete", 
                                                    y="compte", 
                                                    color='pays'
                                                )  
                                    ),

                        ]
                    ),
                    html.Div(
                        className="column is-6",
                        children=[

                            html.H2("Répartition par pays",
                                    style={'textAlign': 'center',
                                           'color': colors['text'],
                                           }),
                            dcc.Graph(
                                id='scatter_chart',
                                figure=px.sunburst(rum, path=["pays", "marque"], color="compte",
                                                hover_data=rum.columns,
                                                values="compte")
                                ),
                        ]
                    ),

                ]),

        ]),


       


    html.Br(),
    html.Br(),


        html.Div(
        className="column is-12 ",
        children=[
            html.Div(
                className="columns",
                children=[
                    html.Div(
                        className="column is-6",
                        children=[
                        
                            dcc.Graph(
                                id='Histo2',
                                figure= px.histogram(origines, 
                                                    x="pays", 
                                                    y="compte", 
                                                    color='pays'
                                                )  
                                        ),
                        ]),

                    html.Div(
                        className="column is-6",
                        children=[                            
                            dcc.Graph(
                                id='pie2',
                                figure=px.sunburst(origines, path=["pays", "compte"], color="compte",
                                            hover_data=origines.columns,
                                            values="compte"))
                        ])

                ])

        ]),

        html.Div(children=[
            html.Iframe(
            id='map',
            srcDoc=open('Producteur_martinique.html', 'r').read(),
            width='80%',
            height='600'
        )
        ])
        
        
])
               



if __name__ == '__main__':
    app.run_server(port= 8050, debug=True)