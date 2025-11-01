import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
File = pd.read_csv("C:/Desktop/DataAnalyticsAssignment/climate change impact on agriculture.csv")
df = pd.DataFrame(File)

# Renaming Columns and changing datatypes
df.rename(columns={'Crop_Type': 'Crop Type', 'Average_Temperature_C': 'Average Temperature(C)',
                   'Total_Precipitation_mm': 'Total Precipitation(mm)', 'CO2_Emissions_MT': 'CO2 Emissions(MT)',
                   'Crop_Yield_MT_per_HA': 'Crop Yield(MT/HA)', 'Extreme_Weather_Events': 'Extreme Weather Events',
                   'Irrigation_Access_%': 'Irrigation Access(%)', 'Pesticide_Use_KG_per_HA': 'Pesticide Use(KG/HA)',
                   'Fertilizer_Use_KG_per_HA': 'Fertilizer Use(KG/HA)', 'Soil_Health_Index': 'Soil Health Index',
                   'Adaptation_Strategies': 'Adaptation Strategies', 'Economic_Impact_Million_USD': 'Economic Impact(Million USD)'}, inplace=True)
df["Year"] = df["Year"].astype("object")

# App title
st.title("🌾 Impact of Climate on Agriculture Explorer 🌍")

# Dataset Overview
st.header("📊 1. Overview of Dataset")

st.subheader("🔍 1.1 Preview Of Dataset")
st.write(df.head())

st.subheader("📈 1.2 Summary of Data Statistics")
st.write(df.describe())

# Sidebar filters
st.sidebar.header("🔧 Filters")
countries = st.sidebar.multiselect("🌐 Select Countries", df['Country'].unique(), default=df['Country'].unique())
crops = st.sidebar.multiselect("🌽 Select Crop Types", df['Crop Type'].unique(), default=df['Crop Type'].unique())
years = st.sidebar.slider("📅 Select Year Range", int(df['Year'].min()), int(df['Year'].max()), (int(df['Year'].min()), int(df['Year'].max())))

# Apply filters
filtered_df = df[
    (df['Country'].isin(countries)) &
    (df['Crop Type'].isin(crops)) &
    (df['Year'] >= years[0]) & (df['Year'] <= years[1])
]

# Display title and data
st.header("📉 2. Visualisation Of The Dataset")
st.subheader("📋 Filtered Dataset")
st.dataframe(filtered_df)

# Plot Crop Yield
colors = ['red', 'blue', 'green', 'darkgreen', 'skyblue', 'purple', 'yellow', 'orange', 'pink', 'hotpink']
st.subheader("🌱 2.1 Crop Yield by Crop Type and Country")
condition_type = st.selectbox("📌 Choose one to visualize:", ["Crop Type", "Country"])
if condition_type == "Crop Type":
    yield_by_crop = filtered_df.groupby("Crop Type")["Crop Yield(MT/HA)"].sum()
    dfc = pd.DataFrame(yield_by_crop)
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=dfc, x=yield_by_crop.index, y=yield_by_crop.values, palette=colors, width=0.5, ax=ax)
    for container in ax.containers:
        ax.bar_label(container)
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)
elif condition_type == "Country":
    yield_by_country = filtered_df.groupby("Country")["Crop Yield(MT/HA)"].sum()
    dfc = pd.DataFrame(yield_by_country)
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=dfc, x=yield_by_country.index, y=yield_by_country.values, palette=colors, width=0.5, ax=ax)
    for container in ax.containers:
        ax.bar_label(container)
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

# Economic Impact
st.subheader("💰 2.2 Economic Impact by Country and Crop Type")
condition_type = st.selectbox("📌 Choose one to visualize:", ["Country", "Crop Type"])
if condition_type == "Country":
    economic_impact = filtered_df.groupby("Country")["Economic Impact(Million USD)"].sum()
    df1 = pd.DataFrame(economic_impact)
    fig, ax = plt.subplots()
    sns.scatterplot(data=df1, x=economic_impact.index, y=economic_impact.values, hue="Country", s=200, ax=ax)
    plt.xticks(rotation=45, ha='right')
    plt.legend(loc="lower right", bbox_to_anchor=(1.3, 0.4))
    st.pyplot(fig)
elif condition_type == "Crop Type":
    economic_impact = filtered_df.groupby("Crop Type")["Economic Impact(Million USD)"].sum()
    df1 = pd.DataFrame(economic_impact)
    fig, ax = plt.subplots()
    sns.scatterplot(data=df1, x=economic_impact.index, y=economic_impact.values, hue="Crop Type", s=200, ax=ax)
    plt.xticks(rotation=45, ha='right')
    plt.legend(loc="lower right", bbox_to_anchor=(1.3, 0.4))
    st.pyplot(fig)

# Climate Insights
st.subheader("🌦️ 2.3 Climate Metrics by Country")
condition_type = st.selectbox("🌡️ Choose a climate indicator:", ["Average Temperature(C)", "Total Precipitation(mm)", "CO2 Emissions(MT)"])
if condition_type == "Average Temperature(C)":
    temp_by_country = filtered_df.groupby("Country")["Average Temperature(C)"].mean()
    fig, ax = plt.subplots()
    ax.pie(temp_by_country, labels=temp_by_country.index, autopct='%1.1f%%', startangle=120)
    ax.set_title("🌡️ Average Temperature(C) by Country")
    st.pyplot(fig)
elif condition_type == "Total Precipitation(mm)":
    precp_by_country = filtered_df.groupby("Country")["Total Precipitation(mm)"].sum()
    fig, ax = plt.subplots()
    ax.pie(precp_by_country, labels=precp_by_country.index, autopct='%1.1f%%', startangle=120)
    ax.set_title("🌧️ Total Precipitation(mm) by Country")
    st.pyplot(fig)
elif condition_type == "CO2 Emissions(MT)":
    co2_by_country = filtered_df.groupby("Country")["CO2 Emissions(MT)"].sum()
    fig, ax = plt.subplots()
    ax.pie(co2_by_country, labels=co2_by_country.index, autopct='%1.1f%%', startangle=120)
    ax.set_title("💨 CO2 Emissions(MT) by Country")
    st.pyplot(fig)

# Agrochemicals & Soil Health
st.subheader("🧪 2.4 Agrochemical Usage and Soil Health")
condition_type = st.selectbox("🧫 Select:", ["Pesticide Use(KG/HA)", "Fertilizer Use(KG/HA)"])
if condition_type == "Pesticide Use(KG/HA)":
    pesti_useby_country = filtered_df.groupby("Country")["Pesticide Use(KG/HA)"].mean()
    soil_healthby_country = filtered_df.groupby("Country")["Soil Health Index"].mean()
    common_countries = pesti_useby_country.index.intersection(soil_healthby_country.index)
    pesti_useby_country = pesti_useby_country.loc[common_countries]
    soil_healthby_country = soil_healthby_country.loc[common_countries]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(pesti_useby_country.index, pesti_useby_country.values, marker='o', label='Pesticide Use (KG/HA)', color='green')
    ax.plot(soil_healthby_country.index, soil_healthby_country.values, marker='s', label='Soil Health Index', color='blue')
    ax.set_title("🌿 Pesticide Use vs Soil Health by Country")
    ax.legend()
    ax.grid(axis='x')
    st.pyplot(fig)
elif condition_type == "Fertilizer Use(KG/HA)":
    ferti_useby_country = filtered_df.groupby("Country")["Fertilizer Use(KG/HA)"].mean()
    soil_healthby_country = filtered_df.groupby("Country")["Soil Health Index"].mean()
    common_countries = ferti_useby_country.index.intersection(soil_healthby_country.index)
    ferti_useby_country = ferti_useby_country.loc[common_countries]
    soil_healthby_country = soil_healthby_country.loc[common_countries]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(ferti_useby_country.index, ferti_useby_country.values, marker='o', label='Fertilizer Use(KG/HA)', color='green')
    ax.plot(soil_healthby_country.index, soil_healthby_country.values, marker='s', label='Soil Health Index', color='blue')
    ax.set_title("🌿 Fertilizer Use vs Soil Health by Country")
    ax.legend()
    ax.grid(axis='x')
    st.pyplot(fig)

# Irrigation Access
st.subheader("🚿 2.5 Irrigation Access by Country and Region")
select_box = st.selectbox("📌 Choose Irrigation Access View:", ["Countrywise", "Regionwise"])
if select_box == "Countrywise":
    irri_accessby_country = filtered_df.groupby("Country")["Irrigation Access(%)"].mean()
    fig, ax = plt.subplots(figsize=(12, 6))
    irri_accessby_country.sort_values().plot(kind='barh', color='teal', ax=ax)
    ax.set_title("🚜 Average Irrigation Access (%) by Country")
    ax.set_xlabel("Irrigation Access (%)")
    ax.set_ylabel("Country")
    st.pyplot(fig)
elif select_box == "Regionwise":
    irri_accessby_regionwise = filtered_df.groupby("Region")["Irrigation Access(%)"].mean()
    fig, ax = plt.subplots(figsize=(12, 6))
    irri_accessby_regionwise.sort_values().plot(kind='barh', color='teal', ax=ax)
    ax.set_title("🏞️ Average Irrigation Access (%) by Region")
    ax.set_xlabel("Irrigation Access (%)")
    ax.set_ylabel("Region")
    st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("👨‍💻 Built By **BARKHA MAHTO**")
