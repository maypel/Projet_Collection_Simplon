from sqlalchemy import create_engine
import psycopg2
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pylab import *

username='postgres'
password=os.environ.get('pg_psw')
port=5432
engine = create_engine(f'postgresql://{username}:{password}@localhost:5432/projet_eau')

df1 = pd.read_sql( """
select
    s.nom_cours_d_eau,
	p.nom_paramètre,
	p.code_paramètre,
    m.résultat_analyse,
    p.symbole_unité_mesure,
    m.date_analyse as date
    
from
    mesures m
join parametres p on
   m.code_paramètre=p.code_paramètre
join stations s on
	s.code_station= m.code_station
where s.nom_cours_d_eau='la Loire' and p.code_paramètre in (1340)
group by s.nom_cours_d_eau, p.code_paramètre, date,m.résultat_analyse
order by p.code_paramètre, date
""", engine)

fig = px.line(df1, x='date', y='résultat_analyse', title='Evolution de la concentration en nitrate de 2018 à 2020')
fig.update_xaxes(rangeslider_visible=True)
fig.show()

df2 = pd.read_sql( """

select
	p.nom_paramètre,
	p.code_paramètre,
    m.résultat_analyse,
    p.symbole_unité_mesure,
    m.date_analyse
    
from
    mesures m
join parametres p on
   m.code_paramètre=p.code_paramètre
join stations s on
	s.code_station= m.code_station
where m.code_fraction_analysée=23 and p.code_paramètre in (1506, 1907, 2766,6894,6895,7729,6865,7727,1191,6660,6853,6854,1832,6381)
group by  p.code_paramètre, m.date_analyse,m.résultat_analyse
order by  p.code_paramètre, m.date_analyse
""", engine)

fig6=px.line(df2,x='date_analyse',y='résultat_analyse',title='Evolution de la concentration des pesticides de 2018 à 2020',color='nom_paramètre',line_group='nom_paramètre',hover_name='nom_paramètre')
fig6.show()

sql_query_00 ="""
select
	p.nom_paramètre,
	p.code_paramètre,
    avg(m.résultat_analyse) as resultat_moyen,
    p.symbole_unité_mesure,
    extract(year from m.date_analyse) as annee,
    count(résultat_analyse) as nombre_de_mesure_par_an
from
    mesures m
join parametres p on
   m.code_paramètre=p.code_paramètre
join stations s on
	s.code_station= m.code_station
where m.code_fraction_analysée=23 and p.code_paramètre in (1108,1506, 1907, 2766,6894,6895,7729,6865,7727,1191,6660,6853,6854,1832,6381)
and extract(year from m.date_analyse) = 2018
group by  p.code_paramètre, annee
order by  p.code_paramètre, annee
"""
results2018 = pd.read_sql_query(sql_query_00, engine)
sql_query_01 = """
select
	p.nom_paramètre,
	p.code_paramètre,
    avg(m.résultat_analyse) as resultat_moyen,
    p.symbole_unité_mesure,
    extract(year from m.date_analyse) as annee,
    count(résultat_analyse) as nombre_de_mesure_par_an
from
    mesures m
join parametres p on
   m.code_paramètre=p.code_paramètre
join stations s on
	s.code_station= m.code_station
where m.code_fraction_analysée=23 and p.code_paramètre in (1108,1506, 1907, 2766,6894,6895,7729,6865,7727,1191,6660,6853,6854,1832,6381)
and extract(year from m.date_analyse) = 2019
group by  p.code_paramètre, annee
order by  p.code_paramètre, annee
"""
results2019 = pd.read_sql_query(sql_query_01, engine)

sql_query_02 = """
select
	p.nom_paramètre,
	p.code_paramètre,
    avg(m.résultat_analyse) as resultat_moyen,
    p.symbole_unité_mesure,
    extract(year from m.date_analyse) as annee,
    count(résultat_analyse) as nombre_de_mesure_par_an
from
    mesures m
join parametres p on
   m.code_paramètre=p.code_paramètre
join stations s on
	s.code_station= m.code_station
where m.code_fraction_analysée=23 and p.code_paramètre in (1108,1506, 1907, 2766,6894,6895,7729,6865,7727,1191,6660,6853,6854,1832,6381)
and extract(year from m.date_analyse) = 2020
group by  p.code_paramètre, annee
order by  p.code_paramètre, annee
"""

results2020 = pd.read_sql_query(sql_query_02, engine)

fig3 = go.Figure(data=[
    go.Bar(name='2018', x=results2018.nom_paramètre, y=results2018.resultat_moyen),
    go.Bar(name='2019', x=results2019.nom_paramètre, y=results2019.resultat_moyen),
    go.Bar(name='2020', x=results2020.nom_paramètre, y=results2020.resultat_moyen)
])
# Change the bar mode
fig3.update_layout(title_text='Moyenne annuelle des taux des pesticides de 2018 à 2020', barmode='group')
fig3.show()

sql_query_03="""
SELECT
    station,
    parametre,
   extract(year from date) as annee,
    resultat,
    limite_de_qualite
FROM qualite_eau qe, parametres p
where qe.parametre=p.nom_paramètre and 
p.code_paramètre in (1108,1506, 1907, 2766,6894,6895,7729,6865,7727,1191,6660,6853,6854,1832,6381)
and extract(year from date) = 2018
group by station, parametre, resultat, date, limite_de_qualite
order by station ;"""

limite2018= pd.read_sql_query(sql_query_03, engine)

del limite2018['parametre']
del limite2018['annee']
del limite2018['station']
limite2018=limite2018.groupby([('limite_de_qualite')]).count()
labels = ['très bon','bon','moyen','médiocre','mauvais']
values = [10672, 4236, 458, 152, 103]

fig4 = go.Figure(data=[go.Pie(labels=labels, values=values,title="Part des limites de qualité pour l'analyse des pesticides en 2018")])
fig4.show()

labels1 = ['très bon','bon','moyen','médiocre','mauvais']
values1 = [11718, 4098, 484, 142, 94]

fig5 = go.Figure(data=[go.Pie(labels=labels1, values=values1,title="Part des limites de qualité pour l'analyse des pesticides en 2019")])
fig5.show()

labels2 = ['très bon','bon','moyen','médiocre','mauvais']
values2 = [4621, 1256, 66, 21, 12]

fig7 = go.Figure(data=[go.Pie(labels=labels2, values=values2,title="Part des limites de qualité pour l'analyse des pesticides en 2020")])
fig7.show()