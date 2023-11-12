import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')


df = pd.read_csv('../Dashboard/hour_clean.csv')

st.set_page_config(page_title="Bike-sharing Dashboard",
                   page_icon="bar_chart:",
                   layout="wide")


def create_season_df(df):
    season_df = df.groupby("season").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    season_df = season_df.reset_index()
    season_df.rename(columns={
        "cnt": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    
    return season_df

def create_working_df(df):
    working_df = df.groupby('workingday').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    working_df = working_df.reset_index()
    working_df.rename(columns ={
        "cnt": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    return working_df

def create_hourly_users_df(df):
    hourly_users_df = df.groupby("hr").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum",
        'weekday': 'unique'
    })
    hourly_users_df = hourly_users_df.reset_index()
    hourly_users_df.rename(columns={
        "cnt": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides",
        'weekday':'day'        
    }, inplace=True)
    
    return hourly_users_df

def create_weather_df(df):
    weather_df = df.groupby('weathersit').agg({
    'casual': 'sum',
    'registered': 'sum',
    'cnt': 'sum'
    }).reset_index()
    weather_df.rename(columns={
    'cnt': 'total_rides',
    'casual': 'casual_rides',
    'registered': 'registered_rides'
}, inplace=True)

    return weather_df

season_df= create_season_df(df)
working_df = create_working_df(df)
hour_df= create_hourly_users_df(df)
weather_df =create_weather_df(df)

with st.sidebar:
    st.image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRRfz5s2e3X65YPVAyO-0XJ6zoe9rUpWS9XUg&usqp=CAU')
    #filter berdasarkan season
    selected_season = st.sidebar.selectbox('Select Season', df['season'].unique())
    filtered_df = df[df['season'] == selected_season]
    st.write(f"Data for {selected_season} season:")
    st.write(filtered_df)


st.header('Dicoding Collection Dashboard 🚲')
    
col1, col2, col3 = st.columns(3)

with col1:
    total_all_rides = df['cnt'].sum()
    st.metric("Total Rides", value=total_all_rides)
with col2:
    total_casual_rides = df['casual'].sum()
    st.metric("Total Casual Rides", value=total_casual_rides)
with col3:
    total_registered_rides = df['registered'].sum()
    st.metric("Total Registered Rides", value=total_registered_rides)

st.markdown("---")
st.subheader('Jumlah Pengguna Sepeda Berdasarkan Musim ')

colors= ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
fig, ax =plt.subplots(figsize=(8,4))
sns.barplot(
    x='season', 
    y='total_rides', 
    data=season_df.sort_values(by='total_rides', ascending=False), 
    errorbar=None, 
    palette=colors,
    ax=ax
    )
ax.set_title('Pengaruh Musim terhadap Jumlah Sewa Sepeda ',loc='center',fontsize=25)
ax.set_ylabel('Jumlah Sewa Sepeda')
ax.set_xlabel('Musim')
ax.tick_params(axis='y', labelsize=15)
ax.tick_params(axis='x', labelsize=10)
st.pyplot(plt)

st.subheader('Jumlah Pengguna Sepeda Hari kerja vs Hari libur')


sns.set(style="whitegrid")
fig2 = plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
sns.boxplot(x='workingday', y='casual_rides', data=working_df, showfliers=False)
plt.title('Distribusi Penyewaan Sepeda Casual (Hari Kerja vs. Libur)')

plt.subplot(2, 2, 2)
sns.boxplot(x='workingday', y='registered_rides', data=working_df, showfliers=False)
plt.title('Distribusi Penyewaan Sepeda Registered (Hari Kerja vs. Libur)')
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)

st.pyplot(fig2)

st.subheader('Pengguna Sepeda Berdasarkan Cuaca')


colors= ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
fig, ax =plt.subplots(figsize=(10,4))
sns.barplot(
    x='weathersit', 
    y='total_rides', 
    data=weather_df.sort_values(by='total_rides', ascending=False), 
    errorbar=None, 
    palette=colors,
    ax=ax
    )
ax.set_title('Pengaruh Cuaca Terhadap Jumlah Sewa Sepeda ',loc='center',fontsize=25)
ax.set_ylabel('Jumlah Sewa Sepeda Harian')
ax.set_xlabel('Cuaca')
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=10)
st.pyplot(plt)