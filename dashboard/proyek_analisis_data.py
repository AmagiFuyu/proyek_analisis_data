import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load data
day_df = pd.read_csv('dashboard/day.csv')
hour_df = pd.read_csv('dashboard/hour.csv')

# Ubah kolom 'dteday' ke tipe data datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'], format='%d/%m/%Y')
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'], format='%d/%m/%Y')

st.title('Dashboard Peminjaman Sepeda 🚲')

st.sidebar.header('Filter')

# Mapping untuk label
season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
weather_mapping = {1: "Cerah", 2: "Mendung", 3: "Hujan Ringan", 4: "Hujan Lebat"}
holiday_mapping = {0: "Tidak", 1: "Ya"}
workingday_mapping = {0: "Tidak", 1: "Ya"}

# memastikan semua opsi cuaca tersedia dalam filter
available_weather = list(set(day_df['weathersit'].unique()).union(weather_mapping.keys()))
available_weather.sort()

# Sidebar Filters
season = st.sidebar.selectbox('Musim', day_df['season'].unique(), format_func=lambda x: season_mapping[x])
weather = st.sidebar.selectbox('Cuaca', available_weather, format_func=lambda x: weather_mapping.get(x, "Tidak Diketahui"))
holiday = st.sidebar.selectbox('Hari Libur', day_df['holiday'].unique(), format_func=lambda x: holiday_mapping[x])
workingday = st.sidebar.selectbox('Hari Kerja', day_df['workingday'].unique(), format_func=lambda x: workingday_mapping[x])
hour = st.sidebar.slider('Jam', min_value=0, max_value=23, value=(0, 23))

# Filter tanggal
start_date = st.sidebar.date_input('Tanggal Mulai', day_df['dteday'].min())
end_date = st.sidebar.date_input('Tanggal Akhir', day_df['dteday'].max())

# Filter data
filtered_day_df = day_df[(day_df['season'] == season) &
                          (day_df['weathersit'] == weather) &
                          (day_df['holiday'] == holiday) &
                          (day_df['workingday'] == workingday) &
                          (day_df['dteday'] >= pd.Timestamp(start_date)) &
                          (day_df['dteday'] <= pd.Timestamp(end_date))]

filtered_hour_df = hour_df[(hour_df['season'] == season) &
                            (hour_df['weathersit'] == weather) &
                            (hour_df['holiday'] == holiday) &
                            (hour_df['workingday'] == workingday) &
                            (hour_df['dteday'] >= pd.Timestamp(start_date)) &
                            (hour_df['dteday'] <= pd.Timestamp(end_date)) &
                            (hour_df['hr'] >= hour[0]) & (hour_df['hr'] <= hour[1])]

# Visualisasi
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

# Visualisasi Peminjaman Sepeda di Hari Libur vs Hari Kerja
st.subheader('Perbandingan Peminjaman Sepeda pada Hari Libur vs Hari Kerja')
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=["Hari Libur", "Hari Kerja"],
            y=[filtered_day_df[filtered_day_df['holiday'] == 1]['cnt'].sum(),
               filtered_day_df[filtered_day_df['workingday'] == 1]['cnt'].sum()],
            ax=ax)
ax.set_ylabel("Jumlah Peminjaman")
ax.set_title("Perbandingan Peminjaman Sepeda")
ax.grid()
st.pyplot(fig)
