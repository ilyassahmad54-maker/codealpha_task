import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page setup
st.set_page_config(page_title="Unemployment Data Dashboard", layout="wide")

st.title("📊 Unemployment Data Analysis Dashboard")
st.write("Interactive dashboard built using Streamlit for internship project.")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("Unemployment_Rate_upto_11_2020.csv")
    df.columns = df.columns.str.strip()
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")

region = st.sidebar.multiselect(
    "Select Region:",
    df["Region"].unique(),
    default=df["Region"].unique()
)

filtered_df = df[df["Region"].isin(region)]

# ------------------ DATA OVERVIEW ------------------
st.subheader("📌 Dataset Overview")

st.write("Shape:", filtered_df.shape)
st.dataframe(filtered_df.head())

# ------------------ KPI METRICS ------------------
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Average Unemployment Rate", round(filtered_df["Estimated Unemployment Rate (%)"].mean(), 2))
col2.metric("Max Unemployment Rate", round(filtered_df["Estimated Unemployment Rate (%)"].max(), 2))
col3.metric("Min Unemployment Rate", round(filtered_df["Estimated Unemployment Rate (%)"].min(), 2))

# ------------------ BAR CHART ------------------
st.subheader("📍 Unemployment Rate by Region")

fig1, ax1 = plt.subplots(figsize=(10,5))

region_data = filtered_df.groupby("Region")["Estimated Unemployment Rate (%)"].mean().sort_values()

region_data.plot(kind="bar", ax=ax1)

plt.xticks(rotation=90)
plt.ylabel("Unemployment Rate")
plt.title("Average Unemployment Rate by Region")

st.pyplot(fig1)

# ------------------ TIME SERIES ------------------
st.subheader("📈 Unemployment Trend Over Time")

time_data = filtered_df.groupby("Date")["Estimated Unemployment Rate (%)"].mean()

fig2, ax2 = plt.subplots(figsize=(10,5))

time_data.plot(ax=ax2)

plt.title("Unemployment Rate Over Time")
plt.ylabel("Rate")

st.pyplot(fig2)

# ------------------ HEATMAP ------------------
st.subheader("🔥 Correlation Heatmap")

fig3, ax3 = plt.subplots(figsize=(8,5))

sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", ax=ax3)

st.pyplot(fig3)

# ------------------ FOOTER ------------------
st.write("✔ Built for Internship Project | Data Science Dashboard")