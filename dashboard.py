import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

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
    weather_user_df = pd.melt(
        weather_user_df,
        id_vars=['weathersit'],
        value_name='Total_user',
        value_vars=['casual_user', 'registered_user'],
        var_name='typr_of_user'
    )
    weather_user_df['weathersit'] = pd.Categorical(weather_user_df['weathersit'],
                                                   categories=['clear','Mist cloudy','light Snow'])
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
        value_name='Total_user')
    
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
        "cnt": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    
    return month_user_df

df = pd.read_csv("https://raw.githubusercontent.com/fikrionii/Dicoding-Bike-Sharing/main/dataset/cleaned_bikeshare_hour.csv")
df['dteday'] = pd.to_datetime(df['dteday'])

min_date = all_df["order_date"].min()
max_date = all_df["order_date"].max()


