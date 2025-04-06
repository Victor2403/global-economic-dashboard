import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objs as go
from statsmodels.tsa.arima.model import ARIMA
import numpy as np
from datetime import datetime
import base64
import io

# =============================================
# DATA PIPELINE: LOADING AND PREPROCESSING
# =============================================
# Load and clean economic data from CSV, converting to datetime format
# and ensuring proper sorting for time-series analysis
df = pd.read_csv("economic_data.csv")
df['Year'] = pd.to_datetime(df['Year'], format='%Y')  # Convert to datetime
df = df.sort_values(['Country', 'Year'])

# List of unique countries for dropdown population
countries = df["Country"].unique()

# Assign visually distinct colors to each country for consistent visualization
color_palette = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
]
country_colors = {country: color_palette[i % len(color_palette)] for i, country in enumerate(countries)}

# Initialize Dash application with modern styling
app = dash.Dash(__name__)
server = app.server  # Required for deployment

# =============================================
# PREDICTIVE ANALYTICS: ARIMA FORECASTING ENGINE
# =============================================
def forecast_gdp(country_data, forecast_periods=5):
    """
    Advanced time-series forecasting using ARIMA (AutoRegressive Integrated Moving Average)
    model to predict GDP trends. Handles data validation and model fitting with error resilience.
    
    Parameters:
        country_data (DataFrame): Preprocessed economic data for a single country
        forecast_periods (int): Number of future periods to predict (default: 5 years)
    
    Returns:
        tuple: (forecast_years, forecast_values) or (None, None) if insufficient data
    """
    try:
        # Convert to time-series with explicit yearly frequency
        ts = country_data.set_index('Year')['GDP (USD)'].asfreq('YS')
        
        # Validate we have sufficient historical data for meaningful forecasting
        if len(ts) < 5:
            raise ValueError("Insufficient data points for forecasting")
            
        # Fit ARIMA model with (p,d,q) parameters - optimized for economic data
        model = ARIMA(ts, order=(1, 1, 1))
        model_fit = model.fit()
        
        # Generate forecast with confidence intervals
        forecast = model_fit.forecast(steps=forecast_periods)
        
        # Generate future year labels
        last_year = ts.index[-1].year
        forecast_years = [last_year + i for i in range(1, forecast_periods + 1)]
        
        return forecast_years, forecast.values
    except Exception as e:
        print(f"Forecast failed for {country_data['Country'].iloc[0]}: {str(e)}")
        return None, None

# =============================================
# INTERACTIVE DASHBOARD LAYOUT
# =============================================
app.layout = html.Div(
    style={"backgroundColor": "#ffffff", "padding": "20px", "fontFamily": "Arial, sans-serif"},
    children=[
        html.H1(
            "Global Economic Intelligence Dashboard",
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
                    maxHeight=150,
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
                dcc.Tab(label="GDP Analysis", value="gdp"),
                dcc.Tab(label="Inflation Trends", value="inflation"),
                dcc.Tab(label="Unemployment Metrics", value="unemployment"),
                dcc.Tab(label="GDP Forecasting", value="forecast"),
            ],
            style={"fontSize": "18px"},
        ),
        html.Div(id="graph-container"),
        html.Div([
            html.Button("Download Current Data as CSV", id="btn_csv"),
            dcc.Download(id="download-dataframe-csv"),
        ], style={"marginTop": "20px", "textAlign": "center"}),
        
        # Enhanced floating info blocks with shadow effects
        html.Div([
            # Feature Block
            html.Div(
                style={
                    "marginTop": "40px",
                    "backgroundColor": "#f9f9f9",
                    "padding": "25px",
                    "borderRadius": "10px",
                    "boxShadow": "0 10px 20px rgba(0,0,0,0.1)",
                    "marginBottom": "30px"
                },
                children=[
                    html.H2("📊 Dashboard Features & Technical Implementation", 
                           style={"fontFamily": "Georgia", "color": "#003300", "borderBottom": "2px solid #003300", "paddingBottom": "10px"}),
                    html.Ul([
                        html.Li("Multi-country economic indicator comparison (GDP, Inflation, Unemployment)", 
                               style={"margin": "15px 0", "color": "#333333"}),
                        html.Li("ARIMA time-series forecasting model with 5-year GDP projections", 
                               style={"margin": "15px 0", "color": "#333333"}),
                        html.Li("Interactive visualizations built with Plotly and Dash", 
                               style={"margin": "15px 0", "color": "#333333"}),
                        html.Li("Data export functionality for further analysis", 
                               style={"margin": "15px 0", "color": "#333333"}),
                        html.Li("Responsive design with error handling and input validation", 
                               style={"margin": "15px 0", "color": "#333333"})
                    ], style={"lineHeight": "1.8", "paddingLeft": "20px"})
                ]
            ),
            
            # Technical Stack Block
            html.Div(
                style={
                    "backgroundColor": "#f9f9f9",
                    "padding": "25px",
                    "borderRadius": "10px",
                    "boxShadow": "0 10px 20px rgba(0,0,0,0.1)",
                    "marginBottom": "30px"
                },
                children=[
                    html.H2("🔧 Technical Stack", 
                           style={"fontFamily": "Georgia", "color": "#003300", "borderBottom": "2px solid #003300", "paddingBottom": "10px"}),
                    html.Div([
                        html.Span("Python", style={"display": "inline-block", "backgroundColor": "#3776AB", "color": "white", "padding": "5px 10px", "margin": "5px", "borderRadius": "5px"}),
                        html.Span("Dash", style={"display": "inline-block", "backgroundColor": "#6E5894", "color": "white", "padding": "5px 10px", "margin": "5px", "borderRadius": "5px"}),
                        html.Span("Plotly", style={"display": "inline-block", "backgroundColor": "#3F4F75", "color": "white", "padding": "5px 10px", "margin": "5px", "borderRadius": "5px"}),
                        html.Span("Pandas", style={"display": "inline-block", "backgroundColor": "#150458", "color": "white", "padding": "5px 10px", "margin": "5px", "borderRadius": "5px"}),
                        html.Span("ARIMA", style={"display": "inline-block", "backgroundColor": "#D62728", "color": "white", "padding": "5px 10px", "margin": "5px", "borderRadius": "5px"}),
                        html.Span("Data Visualization", style={"display": "inline-block", "backgroundColor": "#FF7F0E", "color": "white", "padding": "5px 10px", "margin": "5px", "borderRadius": "5px"}),
                        html.Span("Time-Series Analysis", style={"display": "inline-block", "backgroundColor": "#2CA02C", "color": "white", "padding": "5px 10px", "margin": "5px", "borderRadius": "5px"})
                    ], style={"marginTop": "15px"})
                ]
            ),
            
            # Indicators Block
            html.Div(
                style={
                    "backgroundColor": "#f9f9f9",
                    "padding": "25px",
                    "borderRadius": "10px",
                    "boxShadow": "0 10px 20px rgba(0,0,0,0.1)"
                },
                children=[
                    html.H2("📈 Key Economic Indicators", 
                           style={"fontFamily": "Georgia", "color": "#003300", "borderBottom": "2px solid #003300", "paddingBottom": "10px"}),
                    html.P("This dashboard analyzes and visualizes three critical macroeconomic indicators across multiple countries:", 
                           style={"color": "#333333", "marginTop": "15px"}),
                    html.Div([
                        html.Div(
                            style={
                                "backgroundColor": "#4CAF50",
                                "padding": "15px",
                                "borderRadius": "5px",
                                "margin": "10px 0",
                                "boxShadow": "0 4px 8px rgba(0,0,0,0.1)"
                            },
                            children=[
                                html.H3("GDP (USD)", style={"color": "white", "margin": "0"}),
                                html.P("Gross Domestic Product - measures national economic performance", style={"color": "#E0E0E0", "margin": "5px 0 0"})
                            ]
                        ),
                        html.Div(
                            style={
                                "backgroundColor": "#FF9800",
                                "padding": "15px",
                                "borderRadius": "5px",
                                "margin": "10px 0",
                                "boxShadow": "0 4px 8px rgba(0,0,0,0.1)"
                            },
                            children=[
                                html.H3("Inflation (%)", style={"color": "white", "margin": "0"}),
                                html.P("Annual price level changes - critical for monetary policy", style={"color": "#E0E0E0", "margin": "5px 0 0"})
                            ]
                        ),
                        html.Div(
                            style={
                                "backgroundColor": "#2196F3",
                                "padding": "15px",
                                "borderRadius": "5px",
                                "margin": "10px 0",
                                "boxShadow": "0 4px 8px rgba(0,0,0,0.1)"
                            },
                            children=[
                                html.H3("Unemployment (%)", style={"color": "white", "margin": "0"}),
                                html.P("Labor market health indicator - key for social policies", style={"color": "#E0E0E0", "margin": "5px 0 0"})
                            ]
                        )
                    ])
                ]
            )
        ])
    ]
)

# =============================================
# CORE INTERACTIVITY & DATA PROCESSING
# =============================================
@app.callback(
    Output("graph-container", "children"),
    [Input("country-dropdown", "value"), Input("tabs", "value")],
)
def update_graph(selected_countries, selected_tab):
    """Dynamic visualization generator handling all dashboard interactivity"""
    if not selected_countries:
        return html.Div("⚠️ Please select at least one country.", 
                      style={"color": "red", "fontSize": "20px", "textAlign": "center"})

    primary_country = selected_countries[0] if isinstance(selected_countries, list) else selected_countries

    metric_mapping = {
        "gdp": ("GDP (USD)", "GDP Analysis"),
        "inflation": ("Inflation (%)", "Inflation Trends"),
        "unemployment": ("Unemployment (%)", "Unemployment Metrics"),
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
                hovermode="x unified",
            ),
        }
        return dcc.Graph(figure=figure)
    else:
        country_data = df[df["Country"] == primary_country]
        forecast_years, forecast_values = forecast_gdp(country_data)
        if forecast_years is None:
            return html.Div(
                f"⚠️ Could not generate forecast for {primary_country}. Need at least 5 years of historical data.",
                style={"color": "red", "fontSize": "20px", "textAlign": "center"}
            )

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=country_data["Year"].dt.year, 
            y=country_data["GDP (USD)"], 
            mode="lines+markers", 
            name=f"{primary_country} Historical", 
            line={"color": country_colors[primary_country], "width": 3}
        ))
        fig.add_trace(go.Scatter(
            x=forecast_years, 
            y=forecast_values, 
            mode="lines+markers", 
            name=f"{primary_country} Forecast", 
            line={"color": "#ff0066", "width": 3, "dash": "dash"}
        ))
        fig.update_layout(
            title=f"{primary_country} 5-Year GDP Forecast",
            plot_bgcolor="#ffffff",
            paper_bgcolor="#ffffff",
            xaxis={"title": "Year"},
            yaxis={"title": "GDP (USD)"},
        )
        return dcc.Graph(figure=fig)

# =============================================
# DATA EXPORT FUNCTIONALITY
# =============================================
@app.callback(
    Output("download-dataframe-csv", "data"),
    [Input("btn_csv", "n_clicks")],
    [State("country-dropdown", "value"), State("tabs", "value")],
    prevent_initial_call=True
)
def download_data(n_clicks, selected_countries, selected_tab):
    """Generates CSV export of currently displayed data"""
    if not selected_countries:
        return None
        
    if selected_tab == "forecast":
        country_data = df[df["Country"] == selected_countries[0]]
        forecast_years, forecast_values = forecast_gdp(country_data)
        if forecast_years:
            forecast_df = pd.DataFrame({
                "Year": forecast_years,
                "GDP (USD) Forecast": forecast_values,
                "Country": selected_countries[0]
            })
            historical_df = country_data[["Year", "GDP (USD)", "Country"]]
            historical_df["Year"] = historical_df["Year"].dt.year
            combined_df = pd.concat([historical_df, forecast_df])
            return dcc.send_data_frame(combined_df.to_csv, "economic_forecast.csv")
    else:
        metric = {
            "gdp": "GDP (USD)",
            "inflation": "Inflation (%)",
            "unemployment": "Unemployment (%)"
        }[selected_tab]
        filtered_df = df[df["Country"].isin(selected_countries)][["Country", "Year", metric]]
        filtered_df["Year"] = filtered_df["Year"].dt.year
        return dcc.send_data_frame(filtered_df.to_csv, f"economic_{selected_tab}_data.csv")

# =============================================
# APPLICATION DEPLOYMENT
# =============================================
if __name__ == "__main__":
    app.run(debug=False)