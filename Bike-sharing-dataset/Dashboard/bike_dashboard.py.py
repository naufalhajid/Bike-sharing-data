# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# Load Data
df = pd.read_csv("Bike-sharing-dataset/day.csv")
df['dteday'] = pd.to_datetime(df['dteday'])
df['month'] = df['dteday'].dt.month
df['weekday'] = df['dteday'].dt.day_name()
df['weathersit'] = df['weathersit'].astype(str)

# Judul
st.markdown("<h1 style='text-align: center; color: #2E86AB;'>🚲 Bike Sharing Analytics Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Analisis waktu & cuaca terhadap tren peminjaman sepeda</h4><br>", unsafe_allow_html=True)

# Sidebar Filters
st.sidebar.header("🎛️ Filter Data")
# Mapping angka ke nama bulan
bulan_dict = {
    1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
    5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
    9: "September", 10: "Oktober", 11: "November", 12: "Desember"
}

# Reverse mapping untuk mengambil angka dari nama bulan
nama_ke_angka = {v: k for k, v in bulan_dict.items()}

# Pilihan di sidebar
selected_nama_bulan = st.sidebar.selectbox("📆 Pilih Bulan", [bulan_dict[m] for m in sorted(df['month'].unique())])
selected_month = nama_ke_angka[selected_nama_bulan]

selected_weather = st.sidebar.selectbox("Pilih Cuaca", df['weathersit'].unique())

filtered_df = df[(df['month'] == selected_month) & (df['weathersit'] == selected_weather)]

# Ringkasan
st.markdown("## 📌 Ringkasan Data")
col1, col2, col3 = st.columns(3)
col1.metric("Total Peminjaman", f"{filtered_df['cnt'].sum():,}")
col2.metric("Rata-rata Harian", f"{filtered_df['cnt'].mean():,.2f}")
col3.metric("Hari dengan Peminjaman Tertinggi", filtered_df.loc[filtered_df['cnt'].idxmax(), 'dteday'].strftime('%Y-%m-%d'))

# Chart 1: Peminjaman per Bulan
monthly = df.groupby('month')['cnt'].sum()

# Plot dengan seaborn
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=monthly.index, y=monthly.values, palette='Blues', ax=ax)

# Kustomisasi tampilan
ax.set_title('Jumlah Penyewaan Sepeda per Bulan')
ax.set_xlabel('Bulan')
ax.set_ylabel('Jumlah Penyewaan')
ax.set_xticklabels([
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
st.markdown("## 📅 Peminjaman Sepeda per Bulan")
st.pyplot(fig)

# Chart 2: Distribusi Berdasarkan Cuaca
st.markdown("## 🌤️ Distribusi Peminjaman Berdasarkan Cuaca")

# Buat visualisasi seperti di notebook
fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(data=df_day_cleaned, x='weather', y='count', ax=ax, palette='coolwarm')

# Kustomisasi label dan judul
ax.set_title('Pengaruh Cuaca terhadap Jumlah Penyewaan Sepeda')
ax.set_xlabel('Kondisi Cuaca')
ax.set_ylabel('Jumlah Penyewaan')
ax.set_xticklabels(['Cerah/Clear', 'Berawan', 'Hujan Ringan', 'Hujan Lebat'])

# Tampilkan plot di Streamlit
st.pyplot(fig)


# Chart 3: Tren Harian
st.markdown("## 📈 Tren Harian Penyewaan Sepeda")
st.line_chart(df.set_index('dteday')['cnt'])

# Optional: Tampilkan data mentah
with st.expander("🗃️ Lihat Data Mentah"):
    st.dataframe(filtered_df)
