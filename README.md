# COVID-19-Dashboard
A real-time interactive dashboard providing visual insights into the global spread of COVID-19. This project uses public APIs to fetch data on COVID-19 cases, recoveries, and deaths, and presents the information through intuitive charts and graphs. Built with Python and Streamlit

## 📋 Features

- **Interactive Filters**
  - Date range selection
  - Multi-country selection
  - Dynamic metric selection

- **Key Metrics Display**
  - Total Cases
  - Total Deaths
  - Average Recovery Rate
  - Total Vaccinations

- **Visualizations**
  - 📈 Trend Analysis
    - Multi-metric line charts
    - Time series analysis
  - 🗺 Comparisons
    - Pie charts for distribution
    - Comparative bar charts
  - 📊 Detailed Analysis
    - Correlation scatter plots
    - Correlation heatmaps

- **Data Export**
  - Download data as CSV

## 🚀 Installation

1. Clone the repository:
git clone <repository-url>
cd covid-dashboard

2. Create a virtual environment:
bash
python -m venv venv


3. Activate the virtual environment:
For Windows PowerShell:
bash
.\venv\Scripts\Activate.ps1


4. Install required packages:
bash
pip install streamlit pandas plotly numpy scipy

5. Run the dashboard:
bash
streamlit run covid_dashboard.py

6. Open your web browser and go to:
http://localhost:8501

