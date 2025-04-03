import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
from statsmodels.tsa.arima.model import ARIMA
import numpy as np
from datetime import datetime

# Load and prepare economic data
df = pd.read_csv("economic_data.csv")
df['Year'] = pd.to_datetime(df['Year'], format='%Y')  # Convert to datetime
df = df.sort_values(['Country', 'Year'])

# List of unique countries
countries = df["Country"].unique()

# Initialize Dash app
app = dash.Dash(__name__)

# =============================================
# Improved Forecasting Function
# =============================================
def forecast_gdp(country_data, forecast_periods=5):
    """
    Robust ARIMA forecasting with proper time series handling.
    Returns forecast years and values, or None if insufficient data.
    """
    try:
        # Prepare time series with explicit frequency
        ts = country_data.set_index('Year')['GDP (USD)'].asfreq('YS')
        
        # Need at least 5 data points for meaningful forecast
        if len(ts) < 5:
            raise ValueError("Insufficient data points for forecasting")
            
        # Fit ARIMA model - you can experiment with these parameters
        model = ARIMA(ts, order=(1, 1, 1))
        model_fit = model.fit()
        
        # Generate forecast
        forecast = model_fit.forecast(steps=forecast_periods)
        
        # Create forecast years
        last_year = ts.index[-1].year
        forecast_years = [last_year + i for i in range(1, forecast_periods + 1)]
        
        return forecast_years, forecast.values
    except Exception as e:
        print(f"Forecast failed for {country_data['Country'].iloc[0]}: {str(e)}")
        return None, None

# =============================================
# App Layout
# =============================================
app.layout = html.Div(
    style={"backgroundColor": "#f4f4f4", "padding": "20px"},
    children=[
        html.H1(
            "Global Economic Dashboard",
            style={
                "fontFamily": "Georgia, serif",
                "color": "#006400",
                "textAlign": "left",
                "marginBottom": "20px",
            },
        ),
        html.Div(
            [
                dcc.Dropdown(
                    id="country-dropdown",
                    options=[{"label": country, "value": country} for country in countries],
                    value=["United States"],
                    multi=True,
                    style={
                        "width": "60%",
                        "padding": "10px",
                        "borderRadius": "5px",
                        "boxShadow": "2px 2px 10px rgba(0, 0, 0, 0.2)",
                        "backgroundColor": "#ffffff",
                        "color": "#333333",
                        "border": "1px solid #aaffaa",
                    },
                )
            ],
            style={"textAlign": "center", "marginBottom": "20px"},
        ),
        dcc.Tabs(
            id="tabs",
            value="gdp",
            children=[
                dcc.Tab(label="GDP", value="gdp"),
                dcc.Tab(label="Inflation", value="inflation"),
                dcc.Tab(label="Unemployment", value="unemployment"),
                dcc.Tab(label="GDP Forecast", value="forecast"),
            ],
            style={"fontSize": "18px"},
        ),
        html.Div(id="graph-container"),
    ],
)

# =============================================
# Callback Function
# =============================================
@app.callback(
    Output("graph-container", "children"),
    [Input("country-dropdown", "value"), Input("tabs", "value")],
)
def update_graph(selected_countries, selected_tab):
    if not selected_countries:
        return html.Div("⚠️ Please select at least one country.", style={"color": "red", "fontSize": "20px"})

    primary_country = selected_countries[0] if isinstance(selected_countries, list) else selected_countries

    # Metric configuration
    metric_mapping = {
        "gdp": ("GDP (USD)", "GDP Over Time", "#00cc66"),
        "inflation": ("Inflation (%)", "Inflation Rate Over Time", "#ff6600"),
        "unemployment": ("Unemployment (%)", "Unemployment Rate Over Time", "#3366cc"),
    }

    if selected_tab != "forecast":
        metric, title, color = metric_mapping[selected_tab]
        
        traces = []
        for country in selected_countries:
            filtered_df = df[df["Country"] == country]
            traces.append(
                go.Scatter(
                    x=filtered_df["Year"].dt.year,  # Use just the year for display
                    y=filtered_df[metric],
                    mode="lines+markers",
                    name=country,
                    line={"color": color, "width": 3},
                    marker={"size": 8, "color": "white", "line": {"color": color, "width": 2}},
                )
            )

        figure = {
            "data": traces,
            "layout": go.Layout(
                title=title,
                plot_bgcolor="#f4f4f4",
                paper_bgcolor="#f4f4f4",
                xaxis={"title": "Year", "gridcolor": "#d3d3d3"},
                yaxis={"title": metric, "gridcolor": "#d3d3d3"},
            ),
        }
        return dcc.Graph(figure=figure)
    else:
        # Handle forecast tab
        country_data = df[df["Country"] == primary_country]
        forecast_years, forecast_values = forecast_gdp(country_data)
        
        if forecast_years is None:
            return html.Div(
                f"⚠️ Could not generate forecast for {primary_country}. Need at least 5 years of data.",
                style={"color": "red", "fontSize": "20px"}
            )

        # Historical trace
        historical_trace = go.Scatter(
            x=country_data["Year"].dt.year,
            y=country_data["GDP (USD)"],
            mode="lines+markers",
            name=f"{primary_country} Historical",
            line={"color": "#00cc66", "width": 3},
            marker={"size": 8, "color": "white", "line": {"color": "#00cc66", "width": 2}},
        )

        # Forecast trace
        forecast_trace = go.Scatter(
            x=forecast_years,
            y=forecast_values,
            mode="lines+markers",
            name=f"{primary_country} Forecast",
            line={"color": "#ff0066", "width": 3, "dash": "dash"},
            marker={"size": 10, "symbol": "diamond", "color": "#ff0066"},
        )

        # Confidence interval (example - would need to calculate from ARIMA)
        # You could add this if you want to show forecast uncertainty
        
        fig = go.Figure(data=[historical_trace, forecast_trace])
        fig.update_layout(
            title=f"{primary_country} GDP Forecast (Next 5 Years)",
            plot_bgcolor="#f4f4f4",
            paper_bgcolor="#f4f4f4",
            xaxis={"title": "Year", "gridcolor": "#d3d3d3"},
            yaxis={"title": "GDP (USD)", "gridcolor": "#d3d3d3"},
        )

        return dcc.Graph(figure=fig)

# =============================================
# Run the App
# =============================================
if __name__ == "__main__":
    app.run(debug=False)  # Set debug=False to prevent frequent reloads