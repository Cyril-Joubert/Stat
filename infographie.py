import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import scipy.stats as stats
import numpy as np
import plotly.express as px

df_bonheur = pd.read_csv("/home/cyril.joubert@Digital-Grenoble.local/Documents/module_python/Stat/Data/test_hypo_data/enquete_sur_le_bonheur.csv", sep=";")
df_bonheur["Timestamp"] = pd.to_datetime(df_bonheur["Timestamp"])
df_bonheur = df_bonheur.set_index("Timestamp")


st.title('Infographie sur le dataset du bonheur')

fig = px.pie(names=df_bonheur["Etes vous heureux ?"].value_counts().index, values=df_bonheur["Etes vous heureux ?"].value_counts(), title="Proportion des gens heureux")
st.plotly_chart(fig)



# H0 : les jeunes sont aussi heureux que les vieux
# H1 : les jeunes sont moins heureux que les vieux

df_bonheur_jeunes = df_bonheur.loc[df_bonheur["Quel est votre âge ? (Ex : 30 pour 30 ans)"] <= 30]
df_bonheur_vieux = df_bonheur.loc[df_bonheur["Quel est votre âge ? (Ex : 30 pour 30 ans)"] > 30]

moy_jeunes = df_bonheur_jeunes["Etes vous heureux ?"].mean()
moy_vieux = df_bonheur_vieux["Etes vous heureux ?"].mean()
print(moy_jeunes)
print(moy_vieux)

print(stats.ttest_ind(df_bonheur_jeunes['Etes vous heureux ?'], df_bonheur_vieux['Etes vous heureux ?'], alternative="less"))

# La pvalue est inférieur à 0.05 donc on peut rejeter l'hypothèse H0

fig = px.pie(values=[moy_jeunes, moy_vieux], names=["Jeunes", "Vieux"], title="Comparaison du bonheur entre les jeunes et les vieux")
st.plotly_chart(fig)



fig = px.bar(x=df_bonheur["Accordez-vous de l'importance aux activités créatives ?"].value_counts().index, 
             y=df_bonheur["Accordez-vous de l'importance aux activités créatives ?"].value_counts(), 
             title="Proportion des gens qui accordent de l'importance aux activités créatives"
             )
st.plotly_chart(fig)


print(df_bonheur["Etes vous heureux ?"].corr(df_bonheur["Vous épanouissez-vous dans votre travail ?"]))



# H0 : les gens heureux prennent autant soin de leur santé que les gens malheureux
# H1 : les gens heureux prennent plus soin de leur santé que les gens malheureux

df_bonheur_heureux = df_bonheur.loc[df_bonheur["Etes vous heureux ?"] > 3]
df_bonheur_malheureux = df_bonheur.loc[df_bonheur["Etes vous heureux ?"] <= 3]

moy_sante_heureux = df_bonheur_heureux["Prenez-vous soin de votre santé ?"].mean()
moy_sante_malheureux = df_bonheur_malheureux["Prenez-vous soin de votre santé ?"].mean()
print(moy_sante_heureux)
print(moy_sante_malheureux)

print(stats.ttest_ind(df_bonheur_heureux['Prenez-vous soin de votre santé ?'], df_bonheur_malheureux['Prenez-vous soin de votre santé ?'], alternative="greater"))

# La pvalue est inférieur à 0.05 donc on peut rejeter l'hypothèse H0



fig = go.Figure()

fig = make_subplots(rows=1, cols=2, subplot_titles=["Gens heureux", "Gens malheureux"], specs=[[{'type':'domain'}, {'type':'domain'}]])

fig.add_trace(go.Pie(labels=df_bonheur_heureux["Prenez-vous soin de votre santé ?"].value_counts().index, 
                     values=df_bonheur_heureux["Prenez-vous soin de votre santé ?"].value_counts(),
                     name="Gens heureux"), 1, 1)

fig.add_trace(go.Pie(labels=df_bonheur_malheureux["Prenez-vous soin de votre santé ?"].value_counts().index, 
                     values=df_bonheur_malheureux["Prenez-vous soin de votre santé ?"].value_counts(),
                     name="Gens malheureux"), 1, 2)

fig.update_layout(
    title_text="Comparaison de l'importance apporté à sa santé entre les gens heureux et les gens malheureux",
   )
# fig = px.pie(names=df_bonheur_heureux["Prenez-vous soin de votre santé ?"].value_counts().index , 
#              values=df_bonheur_heureux["Prenez-vous soin de votre santé ?"].value_counts(),  
#              title="Comparaison du soin apporté à sa santé entre les gens heureux et les gens malheureux")
# fig.add_pie()
st.plotly_chart(fig)


