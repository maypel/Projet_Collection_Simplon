#!/usr/bin/python3
from sqlalchemy import create_engine
import psycopg2
import os
import pandas as pd
import folium
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

username='postgres'
password=os.environ.get('pg_psw')
port=5432
engine = create_engine(f'postgresql://{username}:{password}@localhost:5432/collection5')

df1 = pd.read_sql("""Select producteur.nom_producteur, origine.nom, count(produit.nom_produit)
from producteur
inner join origine
on producteur.code_origine = origine.code_origine
inner join produit
on producteur.code_producteur = produit.code_producteur
where origine.nom = 'Martinique'
group by producteur.nom_producteur, origine.nom;
""", engine)


df1.columns = ['producteur', 'origine', 'compte']
                
liste_producteur = ("Hse", "Clement", "La favorite", "Depaz", "Rhum jm", "Trois rivieres", "La mauny", "Dillon", "Neisson", "J. bally", "A 1710", "Saint james", "Hardy", "Grand fond galion")
liste_coords = ([14.69033, -61.01447], [14.6020262, -60.9076566], [14.6354282, -61.0348357], [14.7586626, -61.1658663], [14.86278, -61.13611], [14.47973, -60.96478], 
                [14.50857, -60.9065], [14.61682, -61.04944], [14.69999, -61.17697], [14.78256, -60.99842], [14.58873, -60.86794], [14.78349, -60.99683], [14.76193, -60.91245],
                [14.71778, -60.94698])

dico = {k: v for k, v in zip(liste_producteur, liste_coords)}

dfproducteur = pd.DataFrame(list(zip(liste_producteur, liste_coords)), columns=['producteur', 'coordonnées'])

dfproducteur= dfproducteur.merge(df1)
                  
def map_martinique():
    m = folium.Map(location=[14.65264905851266, -60.99455852290556], zoom_start=11)

    coord = dfproducteur['coordonnées'].tolist()
    producteur = dfproducteur['producteur'].tolist()
    compte = dfproducteur['compte'].tolist()

    for i in range(len(producteur)):
        folium.Marker(location = coord[i], popup = f"{producteur[i]}, {compte[i]}", icon=folium.Icon(color='red')).add_to(m)

    return m

martinique_map = map_martinique()
martinique_map.save('Producteur_martinique.html')

df2 = pd.read_sql("""SELECT producteur.nom_producteur, origine.nom, count(produit.nom_produit)
                  FROM producteur
                  INNER JOIN origine
                  ON producteur.code_origine = origine.code_origine 
                  INNER JOIN produit
                  ON producteur.code_producteur = produit.code_producteur
                  group by producteur.nom_producteur, origine.nom
                  order by count(produit.nom_produit) DESC
                  Limit 10
                  ;
                  """, engine)
                  
dfproducteur1 = df2
dfproducteur1.columns = ['producteur1', 'origine1', 'compte1']


fig2=px.histogram(dfproducteur1,
             x="producteur1", 
             y="compte1", 
             color='origine1'
           )


fig3=px.sunburst(dfproducteur1, path=["origine1", "producteur1"], color="compte1",
           hover_data=dfproducteur1.columns,
           values="compte1")

