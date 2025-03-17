import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# Load data
if os.path.exists("dashboard/day.csv") and os.path.exists("dashboard/hour.csv"):
    day_df = pd.read_csv("dashboard/day.csv")
    hour_df = pd.read_csv("dashboard/hour.csv")
else:
    st.error("File data tidak ditemukan! Pastikan 'day.csv' dan 'hour.csv' tersedia.")

# Ubah kolom 'dteday' ke tipe data datetime
if 'day_df' in locals() and 'hour_df' in locals():
    day_df['dteday'] = pd.to_datetime(day_df['dteday'], format='%d/%m/%Y')
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'], format='%d/%m/%Y')

    st.title('Dashboard Peminjaman Sepeda 🚲')

    st.sidebar.header('Filter')

    # Mapping untuk label
    season_mapping = {0: "All Seasons", 1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    weather_mapping = {0: "All Weathers", 1: "Cerah", 2: "Mendung", 3: "Hujan Ringan", 4: "Hujan Lebat"}
    
    available_seasons = [0] + list(day_df['season'].unique())
    available_weather = [0] + list(day_df['weathersit'].unique())
    available_seasons.sort()
    available_weather.sort()

    # Sidebar Filters
    season = st.sidebar.selectbox('Musim', available_seasons, format_func=lambda x: season_mapping[x])
    weather = st.sidebar.selectbox('Cuaca', available_weather, format_func=lambda x: weather_mapping[x])
    hour = st.sidebar.slider('Jam', min_value=0, max_value=23, value=(0, 23))

    # Filter tanggal
    start_date = st.sidebar.date_input('Tanggal Mulai', day_df['dteday'].min())
    end_date = st.sidebar.date_input('Tanggal Akhir', day_df['dteday'].max())

    # Filter data
    filtered_day_df = day_df[(day_df['dteday'] >= pd.Timestamp(start_date)) &
                              (day_df['dteday'] <= pd.Timestamp(end_date))]
    
    filtered_hour_df = hour_df[(hour_df['dteday'] >= pd.Timestamp(start_date)) &
                                (hour_df['dteday'] <= pd.Timestamp(end_date)) &
                                (hour_df['hr'] >= hour[0]) & (hour_df['hr'] <= hour[1])]
    
    if season != 0:
        filtered_day_df = filtered_day_df[filtered_day_df['season'] == season]
        filtered_hour_df = filtered_hour_df[filtered_hour_df['season'] == season]
    
    if weather != 0:
        filtered_day_df = filtered_day_df[filtered_day_df['weathersit'] == weather]
        filtered_hour_df = filtered_hour_df[filtered_hour_df['weathersit'] == weather]
    
    # Visualisasi 1: Tren Peminjaman Sepeda Sepanjang Tahun
    st.subheader('Tren Peminjaman Sepeda Sepanjang Tahun')
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x=filtered_day_df.groupby("mnth")["cnt"].mean().index,
                 y=filtered_day_df.groupby("mnth")["cnt"].mean().values,
                 marker="o", ax=ax)
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"])
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Rata-rata Jumlah Peminjaman")
    ax.set_title("Tren Peminjaman Sepeda Sepanjang Tahun")
    ax.grid()
    st.pyplot(fig)

    # Visualisasi 2: Pola Peminjaman Sepeda Berdasarkan Jam
    st.subheader('Pola Peminjaman Sepeda Berdasarkan Jam')
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x=filtered_hour_df.groupby("hr")["cnt"].mean().index,
                 y=filtered_hour_df.groupby("hr")["cnt"].mean().values,
                 marker="o", ax=ax)
    ax.set_xlabel("Jam")
    ax.set_ylabel("Rata-rata Jumlah Peminjaman")
    ax.set_title("Pola Peminjaman Sepeda Berdasarkan Jam dalam Sehari")
    ax.grid()
    st.pyplot(fig)

    # Visualisasi 3: Tren Peminjaman Berdasarkan Musim
    st.subheader('Tren Peminjaman Berdasarkan Musim')
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=[season_mapping[s] for s in sorted(day_df['season'].unique())],
                y=[filtered_day_df[filtered_day_df['season'] == s]['cnt'].sum() for s in sorted(day_df['season'].unique())],
                ax=ax)
    ax.set_ylabel("Jumlah Peminjaman")
    ax.set_title("Tren Peminjaman Berdasarkan Musim")
    ax.grid()
    st.pyplot(fig)

    # Visualisasi 4: Tren Peminjaman Berdasarkan Cuaca
    st.subheader('Tren Peminjaman Berdasarkan Cuaca')
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=[weather_mapping[w] for w in sorted(day_df['weathersit'].unique())],
                y=[filtered_day_df[filtered_day_df['weathersit'] == w]['cnt'].sum() for w in sorted(day_df['weathersit'].unique())],
                ax=ax)
    ax.set_ylabel("Jumlah Peminjaman")
    ax.set_title("Tren Peminjaman Berdasarkan Cuaca")
    ax.grid()
    st.pyplot(fig)
