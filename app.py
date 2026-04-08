import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import numpy as np


# Load model
xgb = joblib.load("C:\\Users\\hari om\\model.pkl", 'rb')
# 1. Page Configuration
st.set_page_config(page_title="Global Terrorism", layout="wide", page_icon="🎯")


# Load dataset (for visualization)
df = pd.read_csv("C:\\Users\\hari om\\Downloads\\globalterrorismdb.csv", encoding='latin1') 

# SIDEBAR
with st.sidebar:
    st.image("C:\\Users\\hari om\\Downloads\\images.GT.jpg", width=100)
    st.header("Attack Profile")

    year = st.slider("Year", 1970, 2020, 2010)

    #df is available 
    region = st.selectbox("Region", df['region_txt'].dropna().unique())

    attack_type = st.selectbox("Attack Type", df['attacktype1_txt'].dropna().unique())

    weapon_type = st.selectbox("Weapon Type", df['weaptype1_txt'].dropna().unique())

st.markdown("---")
st.subheader("📊 Advanced Terrorism Insights Dashboard")

#Row1 KPIs
k1, k2, k3, k4 = st.columns(4)

k1.metric("Total Attacks", len(df))
k2.metric("Total Kills", int(df['nkill'].fillna(0).sum()))
k3.metric("Total Wounded", int(df['nwound'].fillna(0).sum()))
k4.metric("Countries Affected", df['country_txt'].nunique())

st.markdown("---")

#Row 2
c1, c2 = st.columns(2)

# Attack by region
with c1:
    region_data = df['region_txt'].value_counts().reset_index()
    region_data.columns = ['Region', 'Count']

    fig1 = px.bar(region_data,
                  x='Region',
                  y='Count',
                  title="Attacks by Region",
                  color='Count')

    st.plotly_chart(fig1, use_container_width=True)

#Attack Types
with c2:
    fig2 = px.pie(df,
                  names='attacktype1_txt',
                  title="Attack Type Distribution")

    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# Row3 
c3, c4 = st.columns(2)

#Attack trend over time
with c3:
    yearly = df.groupby('iyear').size().reset_index(name='attacks')

    fig3 = px.line(yearly,
                   x='iyear',
                   y='attacks',
                   title="Yearly Attack Trend")

    st.plotly_chart(fig3, use_container_width=True)

# Weapon Type Distribution
with c4:
    fig4 = px.histogram(df,
                        x='weaptype1_txt',
                        title="Weapon Type Usage")

    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

st.subheader("🌍 Global Attack Map")

map_df = df[['latitude','longitude', 'nkill', 'country_txt']].dropna()

'''fig_map = px.scatter_mapbox(
    map_df.sample(2000),
    lat="latitude",
    lon="longitude",
    size="nkill",
    zoom=1,
    title="Global Terrorism Map"
)'''

import plotly.express as px

fig_map = px.scatter_mapbox(
    map_df.sample(2000),
    lat="latitude",
    lon="longitude",
    size="nkill",
    color="nkill",
    hover_data=["country_txt", "nkill"],  # ✅ show country name
    zoom=1,
    size_max=15,
    title="Global Terrorism Map",
    mapbox_style="carto-positron"
)

fig_map.update_layout(mapbox_style="carto-darkmatter")

st.plotly_chart(fig_map, use_container_width=True)

country = st.selectbox("Select Country", df['country_txt'].unique())

filtered_df = df[df['country_txt'] == country]

map_df = filtered_df[['latitude','longitude','nkill','country_txt']].dropna()