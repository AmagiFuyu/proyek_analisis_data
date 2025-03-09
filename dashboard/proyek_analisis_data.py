import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
day_df = pd.read_csv("/content/day.csv")
hour_df = pd.read_csv("/content/hour.csv")

# Convert date column
day_df["dteday"] = pd.to_datetime(day_df["dteday"], format='%d/%m/%Y')
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"], format='%d/%m/%Y')

st.title("Dashboard Peminjaman Sepeda 🚴🏻‍♀️")
# Sidebar Date Filter
start_date = st.sidebar.date_input("Start Date", day_df["dteday"].min())
end_date = st.sidebar.date_input("End Date", day_df["dteday"].max())

# Filter data based on date selection
filtered_df = day_df[(day_df["dteday"] >= pd.to_datetime(start_date)) & (day_df["dteday"] <= pd.to_datetime(end_date))]

# Display filtered data
st.write("### Filtered Data Preview", filtered_df.head())

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
season_trend = day_df.groupby("season")["cnt"].mean()
fig, ax = plt.subplots()
sns.boxplot(x="season", y="cnt", data=day_df, ax=ax)
ax.set_xticks([0, 1, 2, 3])
ax.set_xticklabels(["Spring", "Summer", "Fall", "Winter"])
ax.set_xlabel("Musim")
ax.set_ylabel("Jumlah Peminjaman")
ax.set_title("Distribusi Peminjaman Sepeda Berdasarkan Musim")
ax.grid()
st.pyplot(fig)

#Weather trend
st.subheader("Tren Peminjaman Sepeda Berdasarkan Cuaca")
weather_trend = day_df.groupby("weathersit")["cnt"].mean()
fig, ax = plt.subplots()
sns.boxplot(x="weathersit", y="cnt", data=day_df)
ax.set_xticks([0, 1, 2, 3])
ax.set_xticklabels(["Cerah", "Mendung", "Hujan Ringan", "Hujan Lebat"])
ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Jumlah Peminjaman")
ax.set_title("Pengaruh Kondisi Cuaca terhadap Peminjaman Sepeda")
ax.grid()
st.pyplot(fig)
