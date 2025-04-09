# 🌍 Global Economic Intelligence Dashboard

**An interactive dashboard for economic analysis with ARIMA forecasting**  
*Visualizing GDP, inflation, and unemployment trends using World Bank data*

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)
[![Dash](https://img.shields.io/badge/Dash-2.0%2B-FF69B4)](https://dash.plotly.com)
[![ARIMA](https://img.shields.io/badge/Forecasting-ARIMA-yellowgreen)](https://www.statsmodels.org/stable/generated/statsmodels.tsa.arima.model.ARIMA.html)

## 🚀 Key Features
✔ **Multi-Country Economic Analysis**  
- Compare GDP, inflation, and unemployment across 40+ countries  
- Dynamic time-series visualizations (1990-present)  

✔ **Predictive Analytics**  
- ARIMA-based GDP forecasting (5-year projections)  
- Automated data validation and error handling  

✔ **Interactive Dashboard**  
- Country-specific color coding for trends  
- Responsive filters and exportable CSV data  
- Professional UI with floating info cards  

✔ **Optimized Data Pipeline**  
- Efficient CSV data handling with Pandas  
- Cached forecasting results for performance  

## 🛠️ Tech Stack
**Core Technologies**:
- **Python** (Pandas, NumPy, StatsModels)
- **Dash** (Interactive web framework)
- **Plotly** (Advanced visualizations)
- **ARIMA** (Time-series forecasting)

**Key Libraries**:
- `statsmodels` for econometric modeling
- `dash-core-components` for UI elements
- `base64` for data export functionality

## 📊 How It Works
1. **Data Loading**:  
   - Reads economic indicators from `economic_data.csv`
   - Automatically cleans and preprocesses time-series data

2. **Forecasting Engine**:  
   ```python
   def forecast_gdp(country_data):
       # ARIMA modeling with (1,1,1) order
       model = ARIMA(ts, order=(1, 1, 1))
       return model.forecast(steps=5)