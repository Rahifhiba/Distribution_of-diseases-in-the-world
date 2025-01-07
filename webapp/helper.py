import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

COLOR_PRIMARY = "#6e7b91"
COLOR_HIGHLIGHT = "#c2253e"
COLOR_PALETTE = ["#6e7b91", "#c2253e", "#f7f7f7"]

def create_disease_distribution_chart(df, colname, bigtitle, title,xtitle):
    df_counts = df.groupby(['Country', colname]).size().reset_index(name='Count')

    countries = df_counts['Country'].unique()

    fig = go.Figure()

    for country in countries:
        df_country = df_counts[df_counts['Country'] == country]
        max_count = df_country['Count'].max()
        colors = [COLOR_HIGHLIGHT if count == max_count else COLOR_PRIMARY for count in df_country['Count']]
        fig.add_trace(
            go.Bar(
                x=df_country[colname],
                y=df_country['Count'],
                name=country,
                marker=dict(color=colors)
            )
        )

    dropdown_buttons = []
    for i, country in enumerate(countries):
        visibility = [i == j for j in range(len(countries))]
        dropdown_buttons.append(
            {'label': country, 'method': 'update', 'args': [{'visible': visibility}, {'title': f'{title}: {country}'}]}
        )

    fig.update_layout(
        updatemenus=[
            go.layout.Updatemenu(
                active=0,
                buttons=dropdown_buttons,
                direction='down',
                showactive=True,
            )
        ],
        barmode='group',
        title=bigtitle,
        xaxis_title=xtitle,
        yaxis_title='nombre de cas',
    )

    st.plotly_chart(fig)



def get_top_3_diseases(df, colname, title):

    df_counts = df.groupby(['Country', 'Disease Name', 'Disease Category', 'Country label']).size().reset_index(name='Count')
    top_3_diseases = []

    countries = df_counts[colname].unique()

    for country in countries:
        df_country = df_counts[df_counts[colname] == country]
        top_3 = df_country.nlargest(3, 'Count')
        top_3_diseases.append(top_3)

    top_diseases_df = pd.concat(top_3_diseases).reset_index(drop=True)

    fig_pie = px.pie(top_diseases_df, values='Count', names='Disease Name',
                     title=title, facet_col=colname, facet_col_wrap=4, height=800)

    st.plotly_chart(fig_pie)

def get_top_3_diseases_category(df):
    top_3_diseases = []
    country_labels = df["Country label"].unique()

    for label in country_labels:
        df_label = df[df["Country label"] == label]
        df_category_count = df_label.groupby('Disease Category').size().reset_index(name='Count')
        top_3 = df_category_count.nlargest(3, 'Count')
        top_3['Country label'] = label
        top_3_diseases.append(top_3)

    top_diseases_cat_df = pd.concat(top_3_diseases).reset_index(drop=True)

    fig_pie = px.pie(top_diseases_cat_df, values='Count', names='Disease Category',
                     title='Top 3 Disease Categories in Each World Category', facet_col='Country label')
    fig_pie.update_layout(piecolorway=COLOR_PALETTE)
    st.plotly_chart(fig_pie)







