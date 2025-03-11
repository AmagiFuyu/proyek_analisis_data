import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load data
day_df = pd.read_csv("D:\proyek_analisis_data\dashboard\day.csv")
hour_df = pd.read_csv("D:\proyek_analisis_data\dashboard\hour.csv")

# Convert date column
day_df["dteday"] = pd.to_datetime(day_df["dteday"], format='%d/%m/%Y')
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"], format='%d/%m/%Y')

st.title("Dashboard Peminjaman Sepeda 🚴🏻‍♀️")
# Sidebar Date Filter
start_date = st.sidebar.date_input("Start Date", day_df["dteday"].min())
end_date = st.sidebar.date_input("End Date", day_df["dteday"].max())
selected_season = st.sidebar.selectbox("Season", day_df["season"].unique())

# Filter data based on date selection
filtered_df = day_df[
    (day_df["dteday"] >= pd.to_datetime(start_date)) &
    (day_df["dteday"] <= pd.to_datetime(end_date)) &
    (day_df["season"] == selected_season)
]
# Display Metrics
total_rentals = filtered_df["cnt"].sum()
avg_rentals_per_day = filtered_df["cnt"].mean()
st.metric("Total Rentals", total_rentals)
st.metric("Average Rentals per Day", avg_rentals_per_day)

# Clustering
features = ['temp', 'hum', 'windspeed', 'weathersit']
X = day_df[features]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
kmeans = KMeans(n_clusters=3, random_state=42)
day_df['cluster'] = kmeans.fit_predict(X_scaled)

# Visualisasi Cluster
plt.figure(figsize=(8, 6))
sns.scatterplot(x='temp', y='hum', hue='cluster', data=day_df, palette='viridis')
plt.title('Clustering Hasil Peminjaman Sepeda')
plt.xlabel('Suhu')
plt.ylabel('Kelembaban')

# Tampilkan visualisasi di dashboard
st.pyplot(plt)

# Monthly Trend
st.subheader("Tren Peminjaman Sepeda Sepanjang Tahun")
monthly_trend = day_df.groupby("mnth")["cnt"].mean()
fig, ax = plt.subplots()
sns.lineplot(x=monthly_trend.index, y=monthly_trend.values, marker="o", ax=ax)
ax.set_xticks(range(1, 13))
ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"])
ax.set_xlabel("Bulan")
ax.set_ylabel("Rata-rata Jumlah Peminjaman")
ax.set_title("Tren Peminjaman Sepeda")
ax.grid()
st.pyplot(fig)

# Hourly Trend
st.subheader("Pola Peminjaman Sepeda Berdasarkan Jam")
hourly_trend = hour_df.groupby("hr")["cnt"].mean()
fig, ax = plt.subplots()
sns.lineplot(x=hourly_trend.index, y=hourly_trend.values, marker="o", color="orange", ax=ax)
ax.set_xlabel("Jam dalam Sehari")
ax.set_ylabel("Rata-rata Jumlah Peminjaman")
ax.set_title("Pola Peminjaman Sepeda")
ax.set_xticks(range(0, 24))
ax.grid()
st.pyplot(fig)

#Season trend
st.subheader("Tren Peminjaman Sepeda Berdasarkan Musim")
seasonal_rentals = day_df.groupby('season')['cnt'].sum().reset_index()
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x='season', y='cnt', data=seasonal_rentals, ax=ax)
ax.set_xticks([0, 1, 2, 3])
ax.set_xticklabels(["Spring", "Summer", "Fall", "Winter"])
ax.set_xlabel("Musim")
ax.set_ylabel("Jumlah Peminjaman")
ax.set_title("Tren Peminjaman Sepeda Berdasarkan Musim")
ax.grid()
st.pyplot(fig)

#Weather trend
st.subheader("Tren Peminjaman Sepeda Berdasarkan Cuaca")
weather_rentals = day_df.groupby('weathersit')['cnt'].mean().reset_index()
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x='weathersit', y='cnt', data=weather_rentals, ax=ax)
ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Rata-rata Jumlah Peminjaman")
ax.set_title("Pengaruh Kondisi Cuaca terhadap Peminjaman Sepeda")
ax.set_xticks([0, 1, 2, 3])
ax.set_xticklabels(["Cerah", "Mendung", "Hujan Ringan", "Hujan Lebat"])

ax.grid()
st.pyplot(fig)
