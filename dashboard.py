import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

def create_byseason_df(df):
    byseason_df = df.groupby(by="season").cnt.sum().reset_index()
    byseason_df['season'].replace({
        1: 'Spring',
        2: 'Summer',
        3: 'Fall',
        4: 'Winter'
    }, inplace=True)
    byseason_df.rename(columns={
        "cnt": "customer_count"
    }, inplace=True)
    
    return byseason_df

def create_bymonth_df(df):
    filtered_df = df[df["yr"] == 1]
    bymonth_df = filtered_df.groupby(by="mnth").cnt.sum().reset_index()
    bymonth_df['mnth'].replace({
        1: 'Januari',
        2: 'Februari',
        3: 'Maret',
        4: 'April',
        5: 'Mei',
        6: 'Juni',
        7: 'Juli',
        8: 'Agustus',
        9: 'September',
        10: 'Oktober',
        11: 'November',
        12: 'Desember'
    }, inplace=True)
    bymonth_df.rename(columns={
        "cnt": "customer_count",
        "mnth": "month",
    }, inplace=True)
    
    return bymonth_df

def create_month_df(df):
    split_df = df[df["yr"] == 0]
    month_df = split_df.groupby(by="mnth").cnt.sum().reset_index()
    month_df['mnth'].replace({
        1: 'Januari',
        2: 'Februari',
        3: 'Maret',
        4: 'April',
        5: 'Mei',
        6: 'Juni',
        7: 'Juli',
        8: 'Agustus',
        9: 'September',
        10: 'Oktober',
        11: 'November',
        12: 'Desember'
    }, inplace=True)
    month_df.rename(columns={
        "cnt": "customer_count",
        "mnth": "month",
    }, inplace=True)
    
    return month_df

def create_byhour_df(df):
    split_df = df[df["yr"] == 0]
    byhour_df = split_df.groupby(by="hr").cnt.sum().reset_index()
    byhour_df['hr'].replace({
        0: '00.00',
        1: '01.00',
        2: '02.00',
        3: '03.00',
        4: '04.00',
        5: '05.00',
        6: '06.00',
        7: '07.00',
        8: '08.00',
        9: '09.00',
        10: '10.00',
        11: '11.00',
        12: '12.00',
        13: '13.00',
        14: '14.00',
        15: '15.00',
        16: '16.00',
        17: '17.00',
        18: '18.00',
        19: '19.00',
        20: '20.00',
        21: '21.00',
        22: '22.00',
        23: '23.00',
    }, inplace=True)
    byhour_df.rename(columns={
        "cnt": "customer_count",
        "hr": "hour",
    }, inplace=True)

    return byhour_df

def create_hour_df(df):
    filtered_df = df[df["yr"] == 1]
    hour_df = filtered_df.groupby(by="hr").cnt.sum().reset_index()
    hour_df['hr'].replace({
        0: '00.00',
        1: '01.00',
        2: '02.00',
        3: '03.00',
        4: '04.00',
        5: '05.00',
        6: '06.00',
        7: '07.00',
        8: '08.00',
        9: '09.00',
        10: '10.00',
        11: '11.00',
        12: '12.00',
        13: '13.00',
        14: '14.00',
        15: '15.00',
        16: '16.00',
        17: '17.00',
        18: '18.00',
        19: '19.00',
        20: '20.00',
        21: '21.00',
        22: '22.00',
        23: '23.00',
    }, inplace=True)
    hour_df.rename(columns={
        "cnt": "customer_count",
        "hr": "hour",
    }, inplace=True)

    return hour_df

def create_bywindspeed_df(df):
    bywindspeed_df = df.groupby(by="windspeed").cnt.sum().reset_index()
    def categorize_windspeed(windspeed):
        if 0.0 <= windspeed <= 0.0149:
            return 'Calm'
        elif 0.0149 < windspeed <= 0.0448:
            return 'Light Air'
        elif 0.0448 < windspeed <= 0.1045:
            return 'Light Breeze'
        elif 0.1045 < windspeed <= 0.1791:
            return 'Gentle Breeze'
        elif 0.1791 < windspeed <= 0.2686:
            return 'Moderate Breeze'
        elif 0.2686 < windspeed <= 0.3582:
            return 'Fresh Breeze'
        elif 0.3582 < windspeed <= 0.4627:
            return 'Strong Breeze'
        elif 0.4627 < windspeed <= 0.5672:
            return 'Moderate Gale'
        elif 0.5672 < windspeed <= 0.6866:
            return 'Fresh Gale'
        elif 0.6866 < windspeed <= 0.806:
            return 'Strong Gale'
        elif 0.806 < windspeed <= 0.9403:
            return 'Whole Gale'
        elif 0.9403 < windspeed <= 1.075:
            return 'Violent Storm'
        else:
            return 'Unknown'

    bywindspeed_df['windspeed_category'] = bywindspeed_df['windspeed'].apply(categorize_windspeed)
    bywindspeed_grouped = bywindspeed_df.groupby(by="windspeed_category").cnt.sum().reset_index()
    bywindspeed_grouped.rename(columns={
        "cnt": "customer_count",
    }, inplace=True)

    return bywindspeed_grouped

# Load dataset
the_df = pd.read_csv("df_updated.csv")

datetime_columns = ["dteday"]
the_df.sort_values(by="dteday", inplace=True)
the_df.reset_index(inplace=True)

for column in datetime_columns:
    the_df[column] = pd.to_datetime(the_df[column])

# Filter data
min_date = the_df["dteday"].min()
max_date = the_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("BIKE.png",width=250)
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = the_df[(the_df["dteday"] >= str(start_date)) & 
                (the_df["dteday"] <= str(end_date))]

byseason_df = create_byseason_df(main_df)
bymonth_df = create_bymonth_df(main_df)
month_df = create_month_df (main_df)
byhour_df = create_byhour_df (main_df)
hour_df = create_hour_df(main_df)
bywindspeed_grouped = create_bywindspeed_df(main_df)

# Number Of Customer by Season (2011-2012)
st.header('Dashboard Bike Sharing Systems 🚲')
st.subheader('Number of Customer by Season')

col1,col2,col3 = st.columns(3)

with col1:
    total_rentals = byseason_df['customer_count'].sum()
    st.metric("Total rentals", value=total_rentals)

with col2:
    total_registered = main_df['registered'].sum()
    st.metric("Total registered", value=total_registered)

with col3:
    total_casual = main_df['casual'].sum()
    st.metric("Total casual", value=total_casual)

#plot bar chart numbr of customer by season
plt.figure(figsize=(10, 5))

color_ = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    y="customer_count",
    x="season",
    data=byseason_df.sort_values(by="customer_count", ascending=False),
    palette=color_

)
plt.title("Number of Customer by Season", loc="center", fontsize=15)
plt.ylabel("Customer Count")
plt.xlabel("Season")
plt.tick_params(axis='x', labelsize=12)

st.pyplot(plt)

#plot untuk menampilkan Number of Customers per Month in 2011 & 2012
st.subheader('Number of Customers per Month in 2011 & 2012')
plt.figure(figsize=(15, 5))

plt.plot(
    month_df["month"],
    month_df["customer_count"],
    marker='o',
    linewidth=2,
    color="#E32925",
    label="2011"
)
plt.plot(
    bymonth_df["month"],
    bymonth_df["customer_count"],
    marker='o',
    linewidth=2,
    color="#35A047",
    label="2012"
)
plt.title("Number of Customers per Month in 2011 & 2012", loc="center", fontsize=15)
plt.yticks(fontsize=10)
plt.xticks(fontsize=10)
plt.ylabel("Customer Count")
plt.xlabel("Month")
plt.tick_params(axis='x', labelsize=12)
plt.legend()

st.pyplot(plt)

#plot untuk menampilkan Number of Customers per Hour in 2011 & 2012
st.subheader('Number of Customers per Hour in 2011 & 2012')
plt.figure(figsize=(20, 5))

plt.plot(
    byhour_df["hour"],
    byhour_df["customer_count"],
    marker='o',
    linewidth=2,
    color="#E32925",
    label="2011"
)
plt.plot(
    hour_df["hour"],
    hour_df["customer_count"],
    marker='o',
    linewidth=2,
    color="#35A047",
    label="2012"
)
plt.title("Number of Customers per Hour in 2011 & 2012", loc="center", fontsize=15)
plt.yticks(fontsize=10)
plt.xticks(fontsize=10)
plt.ylabel("Customer Count")
plt.xlabel("Hour")
plt.tick_params(axis='x', labelsize=12)
plt.legend()

st.pyplot(plt)

#plot untuk menampilkan Number of Customer by Windspeed
st.subheader('Number of Customer by Windspeed')
plt.figure(figsize=(20, 8))

color_ = ["#D3D3D3", "#D3D3D3", "#D3D3D3","#D3D3D3", "#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3","#D3D3D3"]
bar_plot = sns.barplot(
    x = bywindspeed_grouped['windspeed_category'],
    y = bywindspeed_grouped['customer_count'],
    data=bywindspeed_grouped.sort_values(by="customer_count", ascending=False),
    palette=color_

)

for patch in bar_plot.patches:
    height = patch.get_height()
    bar_plot.text(patch.get_x() + patch.get_width() / 2.0, height + 0.5, f'{height:.0f}', ha='center', va='bottom')
    
plt.title("Number of Customer by Windspeed", loc="center", fontsize=15)
plt.ylabel("Customer Count")
plt.xlabel("Kategori Windspeed")
plt.tick_params(axis='x', labelsize=12)

st.pyplot(plt)



