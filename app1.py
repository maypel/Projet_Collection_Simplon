#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
from sqlalchemy import create_engine
import pandas as pd
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import os

app = dash.Dash(__name__)

external_stylesheets = 'assets/bulma.min.css'

username='postgres'
password=os.environ.get('pg_psw')
port=5432
engine = create_engine(f'postgresql://{username}:{password}@localhost:5432/collection6')


colors = {
    'background': 'yellow',
    'text': 'red'
}
#set the page size
PAGE_SIZE = 10

df1 = pd.read_sql("""select produit.nom_produit, produit.volume, produit.degre, compose.description
from produit
INNER join compose
ON produit.code_produit = compose.code_produit
INNER join collection
ON compose.code_collection = collection.code_collection
INNER join utilisateur
ON collection.code_utilisateur = utilisateur.code_utilisateur
WHERE utilisateur.code_utilisateur = 1;
""", engine)

df2 = pd.read_sql("""SELECT count(compose.code_produit)
FROM compose
INNER join collection
ON compose.code_collection = collection.code_collection
INNER join utilisateur
ON collection.code_utilisateur = utilisateur.code_utilisateur
WHERE utilisateur.code_utilisateur = 1;
""", engine)
for e in df2['count'].items():
    mesure = e[1]

app.layout = html.Div(children= [
        dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True, "hideable": True}
            if i == "iso_alpha3" or i == "year" or i == "id"
            else {"name": i, "id": i, "deletable": True, "selectable": True}
            for i in df1.columns
        ],
        data=df1.to_dict('records'),  # the contents of the table
        editable=True,              # allow editing of data inside all cells
        filter_action="native",     # allow filtering of data by user ('native') or not ('none')
        sort_action="native",       # enables data to be sorted per-column by user or not ('none')
        sort_mode="single",         # sort across 'multi' or 'single' columns
        column_selectable="multi",  # allow users to select 'multi' or 'single' columns
        row_selectable="multi",     # allow users to select 'multi' or 'single' rows
        row_deletable=True,         # choose if user can delete a row (True) or not (False)
        selected_columns=[],        # ids of columns that user selects
        selected_rows=[],           # indices of rows that user selects
        page_action="native",       # all data is passed to the table up-front or not ('none')
        page_current=0,             # page number that user is on
        page_size=6,                # number of rows visible per page
        style_cell={                # ensure adequate header width when text is shorter than cell's text
            'minWidth': 95, 'maxWidth': 95, 'width': 95
        },
        style_cell_conditional=[    # align text columns to left. By default they are aligned to right
            {
                'if': {'column_id': c},
                'textAlign': 'left',
                'color': 'black'
            } for c in ['nom_producteur', 'iso_alpha3']
        ],
        style_data={                # overflow cells' content into multiple lines
            'whiteSpace': 'normal',
            'height': 'auto',
            'color':'blue'
        }
    ),

        html.Br(),

        dbc.Card(
                [
            dbc.CardHeader("Card"),
            dbc.CardBody(
                [
                    html.H4("NOMBRE DE REFERENCES", className="card-title"),
                    html.P(f"{mesure}", className="card-text"),
                ]
             ),
        ],
                 style={
                     "width": "10rem",
                     "height": "10rem",
                     'color': 'red'},
    ),
       



])


# https://github.com/Coding-with-Adam/Dash-by-Plotly/blob/master/DataTable/datatable_intro_and_sort.py

# https://stackoverflow.com/questions/57586258/python-dash-how-to-add-a-kpi-card-component-to-a-dashboard





if __name__ == '__main__':
    app.run_server(port=8049, debug=True)