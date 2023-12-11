import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import scipy.stats as stats
import numpy as np
import plotly.express as px



df_bonheur = pd.read_csv("enquete_sur_le_bonheur.csv", sep=";")
df_bonheur["Timestamp"] = pd.to_datetime(df_bonheur["Timestamp"])
df_bonheur = df_bonheur.set_index("Timestamp")


st.title('Infographie sur le dataset du bonheur')

st.dataframe(df_bonheur, use_container_width=True)

fig = px.pie(names=df_bonheur["Etes vous heureux ?"].value_counts().sort_index(ascending=False).index, 
             values=df_bonheur["Etes vous heureux ?"].value_counts().sort_index(ascending=False), 
             title="Proportion des gens heureux", 
             color=df_bonheur["Etes vous heureux ?"].value_counts().sort_index(ascending=False).index,
             color_discrete_map={5:'lightcyan',
                                 4:'cyan',
                                 3:'royalblue',
                                 2:'darkblue',
                                 1:'black'
                                 }
            )
st.plotly_chart(fig)

st.write("Premier test d'hypothèse :")
st.write("H0 : les jeunes sont aussi heureux que les vieux")
st.write("H1 : les jeunes sont moins heureux que les vieux")


df_bonheur_jeunes = df_bonheur.loc[df_bonheur["Quel est votre âge ? (Ex : 30 pour 30 ans)"] <= 30]
df_bonheur_vieux = df_bonheur.loc[df_bonheur["Quel est votre âge ? (Ex : 30 pour 30 ans)"] > 30]

moy_jeunes = df_bonheur_jeunes["Etes vous heureux ?"].mean()
moy_vieux = df_bonheur_vieux["Etes vous heureux ?"].mean()

st.write("la moyenne des jeunes heureux est de", moy_jeunes)
st.write("la moyenne des jeunes heureux est de", moy_vieux)

pval = stats.ttest_ind(df_bonheur_jeunes['Etes vous heureux ?'], df_bonheur_vieux['Etes vous heureux ?'], alternative="less")

st.write("La pvalue vaut ", pval[1], ", elle est inférieur à 0.05 donc on peut rejeter l'hypothèse H0. On peut donc dire que les jeunes sont moins heureux que les vieux")

fig = px.bar(y=[moy_jeunes, moy_vieux], x=["Jeunes", "Vieux"], title="Comparaison du bonheur entre les jeunes et les vieux")
st.plotly_chart(fig)



fig = px.bar(x=df_bonheur["Accordez-vous de l'importance aux activités créatives ?"].value_counts().index, 
             y=df_bonheur["Accordez-vous de l'importance aux activités créatives ?"].value_counts(), 
             title="Proportion des gens qui accordent de l'importance aux activités créatives",
             height=400
             )
st.plotly_chart(fig)


print(df_bonheur["Etes vous heureux ?"].corr(df_bonheur["Vous épanouissez-vous dans votre travail ?"]))


st.write("Deuxième test d'hypothèse :")
st.write("H0 : les gens heureux prennent autant soin de leur santé que les gens malheureux")
st.write("H1 : les gens heureux prennent plus soin de leur santé que les gens malheureux")

df_bonheur_heureux = df_bonheur.loc[df_bonheur["Etes vous heureux ?"] > 3]
df_bonheur_malheureux = df_bonheur.loc[df_bonheur["Etes vous heureux ?"] <= 3]

moy_sante_heureux = df_bonheur_heureux["Prenez-vous soin de votre santé ?"].mean()
moy_sante_malheureux = df_bonheur_malheureux["Prenez-vous soin de votre santé ?"].mean()

st.write("La moyenne des gens heureux qui prennent soin de leur santé est de", moy_sante_heureux)
st.write("La moyenne des gens malheureux qui prennent soin de leur santé est de", moy_sante_malheureux)

pval2 = stats.ttest_ind(df_bonheur_heureux['Prenez-vous soin de votre santé ?'], df_bonheur_malheureux['Prenez-vous soin de votre santé ?'], alternative="greater")

st.write("La pvalue vaut ", pval2[1], ", elle est inférieur à 0.05 donc on peut rejeter l'hypothèse H0. On peut donc dire que les gens heureux prennent plus soin de leur santé que les gens malheureux")


# fig = go.Figure()

# fig = make_subplots(rows=1, cols=2, subplot_titles=["Gens heureux", "Gens malheureux"], specs=[[{'type':'domain'}, {'type':'domain'}]])

# fig.add_trace(go.Pie(labels=df_bonheur_heureux["Prenez-vous soin de votre santé ?"].value_counts().index, 
#                      values=df_bonheur_heureux["Prenez-vous soin de votre santé ?"].value_counts(),
#                      name="Gens heureux"), 1, 1)

# fig.add_trace(go.Pie(labels=df_bonheur_malheureux["Prenez-vous soin de votre santé ?"].value_counts().index, 
#                      values=df_bonheur_malheureux["Prenez-vous soin de votre santé ?"].value_counts(),
#                      name="Gens malheureux"), 1, 2)

# fig.update_layout(
#     title_text="Comparaison de l'importance apporté à sa santé entre les gens heureux et les gens malheureux",
#    )

df_bonheur_heureux["Prenez-vous soin de votre santé ?"].value_counts()
df_heureux_malheureux = pd.DataFrame()
df_heureux_malheureux["heureux"], df_heureux_malheureux["malheureux"]= df_bonheur_heureux["Prenez-vous soin de votre santé ?"].value_counts(), df_bonheur_malheureux["Prenez-vous soin de votre santé ?"].value_counts()

fig = px.bar(df_heureux_malheureux,
            #  y=df_heureux_malheureux.columns,
             barmode='group',
             height=400)

st.plotly_chart(fig)


