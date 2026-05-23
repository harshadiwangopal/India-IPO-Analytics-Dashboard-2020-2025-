import pandas as pd
import plotly.express as px
import streamlit as st

# Sidebar
st.sidebar.title("About This Project")
st.sidebar.write("Data Source: Chittorgarh IPO Performance Tracker")
st.sidebar.write("Period: 2020 to 2025")
st.sidebar.write("Total IPOs Analyzed: 382 Mainboard IPOs")
st.sidebar.write("Built with: Python, Pandas, Plotly, Streamlit")
st.sidebar.write("By: Harsha Diwangopal")

# Title
st.title("India IPO Analytics Dashboard (2020-2025)")

# Load data
files = {
    '2020': 'data/ipo-performance-mainline-2020.csv',
    '2021': 'data/ipo-performance-mainline-2021.csv',
    '2022': 'data/ipo-performance-mainline-2022.csv',
    '2023': 'data/ipo-performance-mainline-2023.csv',
    '2024': 'data/ipo-performance-mainline-2024.csv',
    '2025': 'data/ipo-performance-mainline-2025.csv',
}

df = []
for key, value in files.items():
    temp = pd.read_csv(value)
    temp['FY'] = key
    df = df + [temp]

master_df = pd.concat(df, ignore_index=True)
master_df.columns = ['company', 'listed_on', 'issue_price', 'listing_close', 'listing_gain', 'current_price', 'profit_loss', 'FY']
master_df['listed_on'] = pd.to_datetime(master_df['listed_on'])
master_df['month'] = master_df['listed_on'].dt.month_name()

# Headline metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total IPOs Analyzed", "382", "2020 to 2025")
col2.metric("Best IPO Ever", "267%", "Sigachi Industries 2021")
col3.metric("Worst IPO Ever", "-27.4%", "Paytm 2021")
col4.metric("Best Year Returns", "39%", "2020 Average")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Year Analysis", "Monthly Trends", "Top & Bottom IPOs"])

# Tab 1 - Overview
with tab1:
    st.subheader("IPO Count by Year")
    ipo_count = master_df.groupby('FY')['company'].count().reset_index()
    ipo_count.columns = ['Year', 'IPO Count']
    fig1 = px.bar(ipo_count, x='Year', y='IPO Count',
                  title='Number of IPOs per Year (2020-2025)',
                  labels={'Year': 'Financial Year', 'IPO Count': 'Number of IPOs'},
                  color='IPO Count',
                  color_continuous_scale='Blues')
    st.plotly_chart(fig1)
    st.write("""
    **Key Finding:** IPO activity surged 575% from 2020 to 2025, but this growth masks a quality problem.
    2021's post-COVID euphoria drove 66 listings with 30% average returns. By 2025, 108 IPOs averaged
    only 9% returns — suggesting market oversaturation and declining listing quality as companies
    rushed to capitalize on retail investor participation.
    """)

# Tab 2 - Year Analysis
with tab2:
    st.subheader("Average Listing Gain by Year")
    avg_listing_gain = master_df.groupby('FY')['listing_gain'].mean().reset_index()
    avg_listing_gain.columns = ['FY', 'avg_listing_gain']
    fig2 = px.bar(avg_listing_gain, x='FY', y='avg_listing_gain',
                  title='Average Listing Gain by Year (2020-2025)',
                  labels={'FY': 'Financial Year', 'avg_listing_gain': 'Avg Gain (%)'},
                  color='avg_listing_gain',
                  color_continuous_scale='Blues')
    st.plotly_chart(fig2)
    st.write("""
    **Key Finding:** 2020 delivered the highest average listing gains (39%) despite having the fewest IPOs.
    2022 and 2025 show the lowest returns at 10% and 9% respectively.
    This inverse relationship between IPO volume and returns suggests that market oversaturation
    directly impacts investor returns — a critical signal for retail investors timing their IPO applications.
    """)

# Tab 3 - Monthly Trends
with tab3:
    st.subheader("Monthly IPO Trends")

    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']

    ipo_by_month = master_df.groupby('month')['company'].count().reset_index()
    ipo_by_month.columns = ['Month', 'IPO Count']
    fig3a = px.bar(ipo_by_month, x='Month', y='IPO Count',
                   title='Number of IPOs per Month (2020-2025)',
                   labels={'Month': 'Month', 'IPO Count': 'Number of IPOs'},
                   color='IPO Count',
                   color_continuous_scale='Blues',
                   category_orders={'Month': month_order})
    st.plotly_chart(fig3a)

    gain_by_month = master_df.groupby('month')['listing_gain'].mean().reset_index()
    gain_by_month.columns = ['Month', 'Avg Gain']
    fig3b = px.bar(gain_by_month, x='Month', y='Avg Gain',
                   title='Average Listing Gain by Month (2020-2025)',
                   labels={'Month': 'Month', 'Avg Gain': 'Avg Listing Gain (%)'},
                   color='Avg Gain',
                   color_continuous_scale='blues',
                   category_orders={'Month': month_order})
    st.plotly_chart(fig3b)

    st.write("""
    **Key Finding:** December dominates IPO activity (59 listings) as companies rush to close
    deals before year end. July delivers the highest average listing gains (36%) —
    mid-year listings tend to be better quality companies with stable market conditions.
    May is the worst month to apply with only 7% average returns.
    """)

with tab4:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🏆 Top 10 Best IPOs")
        top10 = master_df.nlargest(10, 'listing_gain')[['company', 'listing_gain', 'FY']]
        st.dataframe(top10.reset_index(drop=True))
    with col2:
        st.subheader("📉 Top 10 Worst IPOs")
        bottom10 = master_df.nsmallest(10, 'listing_gain')[['company', 'listing_gain', 'FY']]
        st.dataframe(bottom10.reset_index(drop=True))
    st.write("""
    **Key Finding:** Sigachi Industries delivered 267% on listing day in 2021 — the best in 6 years. 
    Paytm remains India's most infamous IPO flop at -27.4%, proving that the largest IPOs 
    are not always the best investments. 2025 dominates the worst performers list, 
    consistent with the declining quality trend identified in Year Analysis.
    """)