import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
day_df = pd.read_csv("/content/day.csv")
hour_df = pd.read_csv("/content/hour.csv")

# Convert date column
day_df["dteday"] = pd.to_datetime(day_df["dteday"], format='%d/%m/%Y', dayfirst=True)
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"], format='%d/%m/%Y', dayfirst=True)

st.title("Analisis Peminjaman Sepeda")

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
