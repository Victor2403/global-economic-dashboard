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

# Assign unique colors to each country
color_palette = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
]
country_colors = {country: color_palette[i % len(color_palette)] for i, country in enumerate(countries)}

# Initialize Dash app
app = dash.Dash(__name__)

# =============================================
# Forecasting Function
# =============================================
def forecast_gdp(country_data, forecast_periods=5):
    try:
        ts = country_data.set_index('Year')['GDP (USD)'].asfreq('YS')
        if len(ts) < 5:
            raise ValueError("Insufficient data points for forecasting")
        model = ARIMA(ts, order=(1, 1, 1))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=forecast_periods)
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
    style={"backgroundColor": "#ffffff", "padding": "20px"},
    children=[
        html.H1(
            "Global Economic Dashboard",
            style={
                "fontFamily": "Escrow, serif",
                "fontSize": "48px",
                "fontWeight": "300",
                "color": "#003300",
                "textAlign": "left",
                "marginBottom": "20px",
                "letterSpacing": "0.5px",
                "lineHeight": "1.2",
                "textTransform": "uppercase"
            }
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

    metric_mapping = {
        "gdp": ("GDP (USD)", "GDP Over Time"),
        "inflation": ("Inflation (%)", "Inflation Rate Over Time"),
        "unemployment": ("Unemployment (%)", "Unemployment Rate Over Time"),
    }

    if selected_tab != "forecast":
        metric, title = metric_mapping[selected_tab]
        traces = []
        for country in selected_countries:
            filtered_df = df[df["Country"] == country]
            traces.append(
                go.Scatter(
                    x=filtered_df["Year"].dt.year,
                    y=filtered_df[metric],
                    mode="lines+markers",
                    name=country,
                    line={"color": country_colors[country], "width": 3, "shape": "spline"},
                    marker={"size": 8, "color": "white", "line": {"color": country_colors[country], "width": 2}},
                )
            )

        figure = {
            "data": traces,
            "layout": go.Layout(
                title=title,
                plot_bgcolor="#ffffff",
                paper_bgcolor="#ffffff",
                xaxis={"title": "Year", "gridcolor": "#d3d3d3"},
                yaxis={"title": metric, "gridcolor": "#d3d3d3"},
            ),
        }
        return dcc.Graph(figure=figure)
    else:
        country_data = df[df["Country"] == primary_country]
        forecast_years, forecast_values = forecast_gdp(country_data)
        if forecast_years is None:
            return html.Div(
                f"⚠️ Could not generate forecast for {primary_country}. Need at least 5 years of data.",
                style={"color": "red", "fontSize": "20px"}
            )

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=country_data["Year"].dt.year, y=country_data["GDP (USD)"], mode="lines+markers", name=f"{primary_country} Historical", line={"color": country_colors[primary_country], "width": 3}))
        fig.add_trace(go.Scatter(x=forecast_years, y=forecast_values, mode="lines+markers", name=f"{primary_country} Forecast", line={"color": "#ff0066", "width": 3, "dash": "dash"}))
        fig.update_layout(title=f"{primary_country} GDP Forecast (Next 5 Years)", plot_bgcolor="#ffffff", paper_bgcolor="#ffffff")
        return dcc.Graph(figure=fig)

# =============================================
# Run App
# =============================================
if __name__ == "__main__":
    app.run(debug=False)