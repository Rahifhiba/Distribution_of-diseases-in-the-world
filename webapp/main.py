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
L’objectif de l’étude est de savoir les maladies les plus courante dans chaque région les différence
de répartition de ces maladies entre les pays développés et les pays en développement ainsi que les
cout de traitement des différent maladies et comment varie-t-il d’un pays à l’autre.
""")

# create_disease_distribution_chart(df, 'Disease Name', 'Répartition des Maladies dans le Monde', 'Répartition des Maladies', 'Maladie')
# create_disease_distribution_chart(df, 'Disease Category', 'Répartition des Catégories de Maladies dans le Monde', 'Répartition des Catégories de Maladies', 'Catégorie de Maladie')

st.subheader('Hipothèses :')
st.write("""
         - Les maladies non transmissibles sont plus fréquentes dans les pays développés.
         - Les maladies infectieuses sont plus fréquentes dans les pays en développement.
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


get_top_3_diseases_category(df)
# tab_top3_disease_incountcat, tab_top3_diseasecat_incountcat = st.tabs(
#     ["Les maladies les plus courantes par catégorie de pays",
#      "Les type de maladies les plus courantes par catégorie de Pays"
#      ]
# )

# with tab_top3_disease_incountcat:
#     st.write("""Les maladies les plus courantes varient considérablement d'un pays à l'autre, par contre,
#              certaines maladies apparaissent fréquemment parmi les trois principales dans plusieurs pays""")
#     get_top_3_diseases(df, "Country", "Top 3 Maladies par Pays")

# # Sélection de l'analyse
# analysis = st.selectbox('Sélectionner une analyse', ('Prévalence des Maladies', 'Coût des Traitements', 'Comparaison Statistique'))

# # Filtrer les pays par catégorie
# country_label = st.selectbox('Sélectionner une catégorie de pays', ('First World country', 'Second World country', 'Third World country'))

# # Exploration de la prévalence des maladies
# if analysis == 'Prévalence des Maladies':
#     st.subheader(f'Prévalence des Maladies - {country_label}')

#     # Filtrer le dataset par catégorie de pays
#     df_filtered = df[df['Country label'] == country_label]

#     # Graphique de la prévalence des maladies par pays
#     fig = px.bar(df_filtered, x='Disease Name', y='Prevalence Rate (%)',
#                  title=f'Taux de Prévalence des Maladies dans les {country_label}')
#     st.plotly_chart(fig)

#     # Boxplot pour comparer les taux de prévalence
#     fig_box = px.box(df_filtered, x='Country label', y='Prevalence Rate (%)',
#                      title='Comparaison des taux de prévalence')
#     st.plotly_chart(fig_box)

# # Exploration des coûts de traitement
# elif analysis == 'Coût des Traitements':
#     st.subheader(f'Coût Moyen des Traitements - {country_label}')

#     # Filtrer le dataset par catégorie de pays
#     df_filtered = df[df['Country label'] == country_label]

#     # Calcul du coût moyen par maladie
#     avg_treatment_cost = df_filtered.groupby(['Disease Name'])['Average Treatment Cost (USD)'].mean().reset_index()

#     # Graphique des coûts moyens
#     fig_cost = px.bar(avg_treatment_cost, x='Disease Name', y='Average Treatment Cost (USD)',
#                      title=f'Coût Moyen des Traitements dans les {country_label}')
#     st.plotly_chart(fig_cost)

# # Test statistique (ANOVA)
# elif analysis == 'Comparaison Statistique':
#     st.subheader('Test ANOVA - Différences de prévalence entre les catégories de pays')

#     # Effectuer le test ANOVA
#     df_anova = df[['Country label', 'Prevalence Rate (%)']]
#     anova_result = stats.f_oneway(
#         df_anova[df_anova['Country label'] == 'First World country']['Prevalence Rate (%)'],
#         df_anova[df_anova['Country label'] == 'Second World country']['Prevalence Rate (%)'],
#         df_anova[df_anova['Country label'] == 'Third World country']['Prevalence Rate (%)']
#     )

#     # Afficher les résultats du test ANOVA
#     st.write(f'Résultat du test ANOVA: F={anova_result.statistic}, p={anova_result.pvalue}')
#     if anova_result.pvalue < 0.05:
#         st.write("Les différences de prévalence entre les catégories de pays sont statistiquement significatives.")
#     else:
#         st.write("Aucune différence significative n'a été trouvée entre les catégories de pays.")

# Recommandations
about = st.sidebar.expander("Explication des categories des maladies")
about.write("""
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

# st.sidebar.title('Explication des categories des maladies')
# st.sidebar
st.sidebar.title('Recommandations')
st.sidebar.write("""
- **Pays Développés** : Encourager la prévention des maladies non transmissibles.
- **Pays en Développement** : Augmenter l'accès aux soins pour les maladies infectieuses.
- **Pays du Tiers-Monde** : Améliorer l'accès aux soins de santé de base.
""")
