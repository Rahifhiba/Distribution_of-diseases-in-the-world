import streamlit as st
import pandas as pd
import plotly.express as px
from scipy import stats
from helper import *
# Charger les données
COLOR_PRIMARY = "#6e7b91"
COLOR_HIGHLIGHT = "#c2253e"
COLOR_PALETTE = ["#c2253e","#6e7b91", "#f7f7f7"]

@st.cache_data
def load_data():
    df = pd.read_csv('final.csv')  # Remplace par le chemin de ton fichier
    return df

df = load_data()

# Titre de l'application
st.title('Analyse de la répartition des maladies Mondialement en 2024')
st.write(df)

st.subheader('Objectif de l\'étude :')
# Description
st.write("""
L'objectif de l'étude est de savoir quelles sont les maladies les plus courantes dans les différents pays et
Comment elles sont réparties entre les différentes catégories des pays (dévelopé, en cours de développement, tiers monde).
""")

# create_disease_distribution_chart(df, 'Disease Name', 'Répartition des Maladies dans le Monde', 'Répartition des Maladies', 'Maladie')
# create_disease_distribution_chart(df, 'Disease Category', 'Répartition des Catégories de Maladies dans le Monde', 'Répartition des Catégories de Maladies', 'Catégorie de Maladie')

st.subheader('Hypothèses :')
st.write("""
         - Les maladies non transmissibles sont plus fréquentes dans les pays développés.
         - Les maladies infectieuses sont plus fréquentes dans les pays en développement.
         - il y a une différence significative dans les taux de prévalence des maladies entre les pays développés et les pays en développement.
         """)
st.subheader('Visualisation :')

tab_distribution_disease, tab_distribution_disease_cat = st.tabs(
    [
        "Répartition des Maladies dans le Monde",
        "Répartition des Catégories de Maladies dans le Monde",
    ]
)
with tab_distribution_disease:
    st.write("la répartition des cas de maladies varie considérablement entre les différentes maladies et les différents pays.")
    create_disease_distribution_chart(df, 'Disease Name', 'Répartition des Maladies dans le Monde', 'Répartition des Maladies', 'Maladie')

with tab_distribution_disease_cat:
    st.write("On remarque que les maladies viral sont les plus répandues dans le monde.")
    create_disease_distribution_chart(df, 'Disease Category', 'Répartition des Catégories de Maladies dans le Monde', 'Répartition des Catégories de Maladies', 'Catégorie de Maladie')



fig = px.pie(df, names='Country label', title='Répartition des Pays par Catégorie', hole=0.5)
fig.update_layout(piecolorway=COLOR_PALETTE,)
st.plotly_chart(fig)
st.write("""Cette distribution montre que l'ensemble des données n'est pas équilibré en termes de représentation des différentes catégories de pays. Ce déséquilibre peut être dû à plusieurs facteurs :
- Les pays du premier monde bénéficient de meilleurs systèmes de suivi des maladies et d'études sanitaires plus approfondies, ce qui se traduit par un volume plus important de données enregistrées.
- Les pays du second monde pourraient être sous-représentés car ils ne disposent pas de l'infrastructure de suivi des maladies des pays du premier monde et ne bénéficient pas du même niveau d'attention mondiale que les pays du tiers monde.
- Les pays du tiers monde pourraient être plus représentés en raison des efforts de recherche mondiaux axés sur les maladies tropicales et infectieuses qui affectent ces régions de manière disproportionnée.
Ce déséquilibre souligne l'importance de prendre en compte les biais dans la collecte des données lors de l'interprétation des statistiques sanitaires mondiales.
""")


tab_top3_disease, tab_top3_disease_per_world = st.tabs(
    ["Les maladies les plus courantes par pays",
     "Les maladies les plus courantes par catégorie de Pays"
     ]
)
with tab_top3_disease:
    st.write("""Les maladies les plus courantes varient considérablement d'un pays à l'autre, par contre,
             certaines maladies apparaissent fréquemment parmi les trois principales dans plusieurs pays""")
    get_top_3_diseases(df, "Country", "Top 3 Maladies par Pays")
with tab_top3_disease_per_world:
    st.write("""Le cancer est présent dans les pays du premier monde et tiers monde, tandis que l'hépatite est plus présente dans les pays du premier et second monde.""")
    get_top_3_diseases(df, "Country label", "Top 3 Maladies par Catégorie de Pays")


st.write("""
         Ce graphe montre que les maladies virales sont les plus courantes dans toutes les catégories de pays,
         suivies par les maladies bactériennes et enfin les maladies neurologiques. Cela suggère que les efforts
         de santé publique devraient se concentrer en priorité sur la prévention et le traitement des maladies virales,
         tout en n'oubliant pas l'importance des maladies bactériennes et neurologiques.
         """)
get_top_3_diseases_category(df)
st.write("""le type de maladie le plus répandu dans tous les pays sont les maladies virales, suivies des maladies bactériennes et neurologiques.""")

prevalence_graph(df)
st.write("""
        les pays développés ont une distribution légèrement plus dispersée et incluent des cas avec une prévalence plus élevée.
        Cela pourrait indiquer des différences dans la manière dont certaines maladies sont répandues ou signalées dans les deux groupes de pays.
""")


# Filtrer les données pour les pays ayant des taux de prévalence significatifs

# Test ANOVA pour comparer les taux de prévalence entre les catégories de pays
st.subheader('Comparaison Statistique (ANOVA test)')
st.write("""**Hypothèse Nulle et Hypothèse Alternative:**
- Hypothèse nulle (H0) : Les taux de prévalence moyens entre les différents groupes de pays sont les mêmes.
- Hypothèse alternative (H1) : Les taux de prévalence moyens entre les différents groupes de pays sont différents.""")
df_anova = df[['Country label', 'Prevalence Rate (%)']]

# Regrouper les catégories
df_anova['Country label'] = df_anova['Country label'].replace({'Second World country': 'Developing World', 'Third World country': 'Developing World'})

anova_result = stats.f_oneway(
    df_anova[df_anova['Country label'] == 'First World country']['Prevalence Rate (%)'],
    df_anova[df_anova['Country label'] == 'Developing World']['Prevalence Rate (%)']
)

st.write(f"""
**Résultats du test ANOVA :**
- **F-statistique** : {anova_result.statistic:.4f}
- **p-value** : {anova_result.pvalue:.4f}
""")
if anova_result.pvalue < 0.05:
    st.write("Les différences de prévalence entre les catégories de pays sont statistiquement significatives, on rejet donc l'hypothèse nulle.")
else:
    st.write("""Aucune différence significative n'a été trouvée entre les catégories de pays,
             nous concluons qu'on ne peut pas rejeter l'hypothèse nulle.""")

# Recommandations

st.sidebar.title('Recommandations')
st.sidebar.write("""
- **Pour les pays Développés** : Encourager la prévention des maladies virales grâce à des compagnes de vaccination et de sentsibilisation.
- **Pour les pays en Développement** : Augmenter l'accès aux soins pour les maladies infectieuses.
- **Pour les pays du Tiers-Monde** : Améliorer l'accès aux soins de santé de base.
""")

explication = st.sidebar.expander("Explication de types des maladies")
explication.write("""
- **Viral :** Maladies causées par des virus.
- **Parasitic :** Maladies causées par des parasites.
- **Genetic :** Maladies liées à des anomalies génétiques.
- **Chronic :** Maladies persistantes nécessitant un suivi à long terme.
- **Metabolic :** Maladies affectant le métabolisme du corps.
- **Autoimmune :** Maladies où le système immunitaire attaque le corps.
- **Cardiovascular :** Maladies touchant le cœur et les vaisseaux sanguins.
- **Respiratory :** Maladies affectant le système respiratoire.
- **Bacterial :** Maladies causées par des bactéries.
- **Infectious :** Maladies transmissibles, souvent d'origine virale ou bactérienne.
- **Neurological :** Maladies affectant le système nerveux.
""")
source = st.sidebar.expander("Source de données")
source.write("""[Global health statistics](https://www.kaggle.com/datasets/malaiarasugraj/global-health-statistics/data)""")
