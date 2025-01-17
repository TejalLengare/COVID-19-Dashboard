import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots

# Basic page config
st.set_page_config(page_title="COVID-19 Dashboard", layout="wide")
st.title("🦠 COVID-19 Dashboard")
st.markdown("### Interactive Analytics Dashboard")

# Create sample data with more variables
def create_sample_data():
    dates = pd.date_range(start='2020-01-01', end='2023-12-31', freq='D')
    n = len(dates)
    
    countries = ['USA', 'India', 'Brazil', 'UK', 'France']
    data = []
    
    for country in countries:
        cases = np.random.randint(1000, 2000, size=n)
        deaths = np.random.randint(100, 1100, size=n)
        recovered = np.random.randint(500, 1500, size=n)
        active = cases - deaths - recovered
        vaccination = np.cumsum(np.random.randint(100, 1000, size=n))
        
        for i in range(n):
            data.append({
                'date': dates[i],
                'country': country,
                'cases': cases[i],
                'deaths': deaths[i],
                'recovered': recovered[i],
                'active': active[i],
                'vaccination': vaccination[i],
                'recovery_rate': (recovered[i] / cases[i]) * 100,
                'mortality_rate': (deaths[i] / cases[i]) * 100
            })
    
    return pd.DataFrame(data)

# Load data
df = create_sample_data()

# Sidebar filters
st.sidebar.header("📊 Filters")
selected_countries = st.sidebar.multiselect(
    "Select Countries",
    options=df['country'].unique(),
    default=df['country'].unique()[:3]
)

date_range = st.sidebar.date_input(
    "Select Date Range",
    [df['date'].min(), df['date'].max()]
)

# Filter data
mask = (
    (df['date'] >= pd.to_datetime(date_range[0])) & 
    (df['date'] <= pd.to_datetime(date_range[1])) &
    (df['country'].isin(selected_countries))
)
filtered_df = df.loc[mask]

# Display metrics in a more attractive way
st.markdown("### 📈 Key Metrics")
col1, col2, col3, col4 = st.columns(4)
with col1:
    total_cases = filtered_df.groupby('country')['cases'].sum().sum()
    st.metric("Total Cases", f"{total_cases:,.0f}")
with col2:
    total_deaths = filtered_df.groupby('country')['deaths'].sum().sum()
    st.metric("Total Deaths", f"{total_deaths:,.0f}")
with col3:
    avg_recovery = filtered_df['recovery_rate'].mean()
    st.metric("Avg Recovery Rate", f"{avg_recovery:.2f}%")
with col4:
    total_vaccinated = filtered_df.groupby('country')['vaccination'].last().sum()
    st.metric("Total Vaccinated", f"{total_vaccinated:,.0f}")

# Create tabs for different visualizations
tab1, tab2, tab3 = st.tabs(["📈 Trends", "🗺 Comparisons", "📊 Detailed Analysis"])

with tab1:
    # Line chart with multiple metrics
    st.subheader("Disease Progression Over Time")
    metrics = st.multiselect(
        "Select metrics to display",
        ['cases', 'deaths', 'recovered', 'active'],
        default=['cases', 'deaths']
    )
    
    fig = go.Figure()
    for metric in metrics:
        for country in selected_countries:
            country_data = filtered_df[filtered_df['country'] == country]
            fig.add_trace(go.Scatter(
                x=country_data['date'],
                y=country_data[metric],
                name=f"{country} - {metric}",
                mode='lines'
            ))
    
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie chart for distribution
        st.subheader("Case Distribution by Country")
        fig_pie = px.pie(
            filtered_df.groupby('country')['cases'].sum().reset_index(),
            values='cases',
            names='country',
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Bar chart comparing metrics
        st.subheader("Country-wise Comparison")
        metric_to_compare = st.selectbox(
            "Select metric",
            ['cases', 'deaths', 'recovered', 'active', 'vaccination']
        )
        fig_bar = px.bar(
            filtered_df.groupby('country')[metric_to_compare].sum().reset_index(),
            x='country',
            y=metric_to_compare,
            color='country'
        )
        st.plotly_chart(fig_bar, use_container_width=True)

with tab3:
    # Scatter plot without trend line
    st.subheader("Correlation Analysis")
    x_axis = st.selectbox("Select X-axis metric", ['cases', 'deaths', 'recovered', 'active'])
    y_axis = st.selectbox("Select Y-axis metric", ['deaths', 'cases', 'recovered', 'active'])
    
    fig_scatter = px.scatter(
        filtered_df,
        x=x_axis,
        y=y_axis,
        color='country',
        title=f"{x_axis.title()} vs {y_axis.title()}"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Heatmap of correlations
    st.subheader("Correlation Heatmap")
    correlation_data = filtered_df[['cases', 'deaths', 'recovered', 'active', 'vaccination']].corr()
    fig_heatmap = px.imshow(
        correlation_data,
        color_continuous_scale='RdBu_r',
        aspect='auto'
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

# Add detailed data table with download button
st.markdown("### 📋 Detailed Data")
st.download_button(
    label="Download data as CSV",
    data=filtered_df.to_csv(index=False).encode('utf-8'),
    file_name='covid_data.csv',
    mime='text/csv',
)
st.dataframe(filtered_df)