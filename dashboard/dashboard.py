import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
from babel.numbers import format_currency
sns.set(style='dark')



df = pd.read_csv("https://raw.githubusercontent.com/AlgiA3/Dicoding-project/main/clean_day_df.csv")
df['dteday'] = pd.to_datetime(df['dteday'])
#create helper function
def create_weathersit_user_df(df):
    weather_user_df = df.groupby('weathersit').agg({
        'casual':'sum',
        'registered': 'sum',
        'cnt': 'sum'
    })
    weather_user_df = weather_user_df.reset_index()
    weather_user_df.rename(columns ={
        'casual': 'casual_user',
        'registered': 'registered_user',
        'cnt':'total_user'
    },inplace=True)
    weather_user_df = pd.melt(weather_user_df,
                                      id_vars=['weathersit'],
                                      value_vars=['casual_user', 'registered_user'],
                                      var_name='type_of_user',
                                      value_name='count_user')
   
    weather_user_df['weathersit'] = pd.Categorical(weather_user_df['weathersit'],
                                                   categories=['Clear','Mist cloudy','Light Snow'])
    weather_user_df= weather_user_df.sort_values('weathersit')
    return weather_user_df

def  create_season_df(df):
    season_df = df.groupby("season").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    season_df = season_df.reset_index()
    season_df.rename(columns={
        "cnt": "total_user",
        "casual": "casual_user",
        "registered": "registered_user"
    }, inplace=True)
    
    season_df = pd.melt(
        season_df,
        id_vars=['season'],
        value_vars=['casual_user', 'registered_user'],
        var_name='type_of_user',
        value_name='count_user')
    
    season_df['season'] = pd.Categorical(season_df['season'],
                                             categories=['Spring', 'Summer', 'Fall', 'Winter'])
    season_df = season_df.sort_values('season')
    
    return season_df

def create_month_user(df):
      # Resample data berdasarkan bulan
    month_user_df = df.resample(rule='M', on='dteday').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    month_user_df.index = month_user_df.index.strftime('%b-%y')
    month_user_df = month_user_df.reset_index()
    month_user_df.rename(columns={
        "dteday": "yearmonth",
        "cnt": "total_user",
        "casual": "casual_user",
        "registered": "registered_user"
    }, inplace=True)
    
    return month_user_df



min_date = df["dteday"].min()
max_date = df["dteday"].max()

# ----- SIDEBAR -----
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://www.sepeda.me/wp-content/uploads/2019/05/Sepeda-balap-TT-triathlon-Cervelo-P5X.jpg")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Date',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
    main_df = df[(df["dteday"] >= str(start_date)) & 
                (df["dteday"] <= str(end_date))]
    
    
weather_user_df = create_weathersit_user_df(main_df)
season_user_df = create_season_df(main_df)
month_user_df = create_month_user(main_df)


st.header('Bike Sharing Dicoding :bicyclist:')

# -----chart------
st.subheader("Users Bike Sharing")
 

 
fig = px.bar(weather_user_df,
              x='weathersit',
              y='count_user',  
              color='type_of_user',
              barmode='group',
              color_discrete_sequence=["skyblue", "orange", "red"],
              title='Count of bikeshare rides by weather').update_layout(xaxis_title='', yaxis_title='Total Rides')

st.plotly_chart(fig, use_container_width=True)

fig = px.bar(season_user_df,
              x='season',
              y='count_user',  
              color='type_of_user',
              barmode='group',
              color_discrete_sequence=["skyblue", "orange", "red"],
              title='Count of bikeshare rides by season').update_layout(xaxis_title='', yaxis_title='Total Rides')
st.plotly_chart(fig, use_container_width=True)

fig = px.bar(month_user_df,
              x='yearmonth',
              y=[ 'casual_user','registered_user'],  
              color='total_user',
              barmode='group',
              color_discrete_sequence=["skyblue", "orange", "red"],
              title='Count of bikeshare rides by Month').update_layout(xaxis_title='', yaxis_title='Total Rides')
st.plotly_chart(fig, use_container_width=True)
