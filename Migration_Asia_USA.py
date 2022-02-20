#import packages
from itertools import groupby
import streamlit as st
import pandas as pd
import plotly
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    layout="centered",
    page_icon="🌏",
    menu_items={
    'About': "#In an ideal world, I would redirect you to another page. 🧐"
    }
)

#play around with the background a little
def set_bg_hack_url():
    '''
    A function to unpack an image from url and set as bg.
    Returns
    -------
    The background.
    '''
        
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url("https://images.unsplash.com/photo-1451187580459-43490279c0fa?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1744&q=80");
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

set_bg_hack_url()

#title (centered), load CSV file
st.markdown("<h1 style='text-align: center; color: yellow;'>Migration from Asian Countries to the United States of America</h1>", unsafe_allow_html=True)

#@st.cache needed??
#Create a subheader with a different background than a transparent one
st.subheader('Raw data')
def load_data(nrows):
    data = pd.read_csv('https://datasetssja38.s3.amazonaws.com/Asia_USA_Migration_Data_Coord3.csv', nrows=nrows) 
    return data
data = load_data(5000)

df = data.style.set_properties(**{'background-color': 'black','color': 'white'})
st.write(df)

#Migration histogram
data["Population"].replace({"..": "0"}, inplace=True)
st.subheader('')
st.subheader('Overall migration per country across years')
datamap = [go.Bar(x=data.Country,
y=data['Population'].astype(float))]
layout = go.Layout(title="Total Migration from Asian Countries to the USA",
xaxis=dict(title='Country'),
yaxis=dict(title='Migration'))
fig = go.Figure(data=datamap, layout=layout)
st.plotly_chart(fig)

with st.expander("See explanation"):
     st.write("""
         I think it's not surprising to see that the countries with the 
         largest population in Asia have the highest immigration rates. 
         China and India are the top two, as you can see from the histogram
     """)

#quick cleaning 
st.subheader('')
st.subheader("Countries in Asia")
data.rename(columns={'Latitude': 'lat', 'Longitude': 'lon', 'ISOCode': 'ISO-3'}, inplace=True)
df = pd.DataFrame(data, columns=['lat', 'lon'])



st.map(df, zoom=None, use_container_width=True)
#Remove first 5 characters from the ISO-3 column
data['ISO-3'] = data['ISO-3'].str[5:]

#Choropleth map
st.subheader('')
st.subheader("Map indicating volume of immigration levels per country, over time")
fig2 = go.Figure(px.choropleth(data,
locations = 'ISO-3',
color=data["Population"].astype(float),
animation_frame="Year",
color_continuous_scale="reds", 
hover_name='Country',
locationmode='ISO-3',
scope="asia",
title='Immigration from Asian countries to the USA (2004-2013)',
height=600
))

fig2.update_layout(mapbox_style="carto-positron")
st.plotly_chart(fig2)

with st.expander("See explanation"):
     st.write("""
         Over time, it's clear to see that while India's immigration rates fall,
         you see an increase in Middle Eastern countries' immigration rates. 
         Iraq's increase, for example, can be attributed to the 2003 US Invasion.
     """)

#import cleaned CSV map with GDP per capita
final_df = pd.read_csv('https://datasetssja38.s3.amazonaws.com/Asia_USA_Immigration_Final.csv')
final_df = final_df.replace('..', '0')

st.subheader('')
st.subheader("Scatterplot visualizing potential correlations between country's immigration levels and GDP per capita")
#scatterplot 
fig3 = px.scatter(final_df, x="CapitaGDP", y=final_df["Population"].astype(float), animation_frame="Year", animation_group="Country",
size=final_df["Population"].astype(float), color="RegName", hover_name="Country")
fig3.update_layout(
    height=800,
    title_text='Immigration to the USA from Asia, and GDP Per Capita',
    yaxis_title = "Immigration",
    xaxis_title = "GDP Per Capita"
    )
st.plotly_chart(fig3)

with st.expander("See explanation"):
     st.write("""
         Lastly, I think it's obvious that countries with lower GDP per capita, 
         are more likely to immigrate to the US than countries like Singapore, the UAE, Japan, and others.
     """)

#include download csv button

def convert_df(data):
    return data.to_csv().encode('utf-8')

csv1 = convert_df(data)
csv2 = convert_df(final_df)

st.subheader("Would you like to download the datasets and experiment with them yourself?")

st.download_button(
     label="Download original dataset as CSV",
     data=csv1,
     file_name='Asia_USA_Migration_Data_Original.csv',
     mime='text/csv',
 )

st.download_button(
     label="Download cleaned dataset as CSV",
     data=csv2,
     file_name='Asia_USA_Migration_Data_Original.csv',
     mime='text/csv',
 )
