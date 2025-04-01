import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Load GDP data
df = pd.read_csv("gdp_data.csv")

# Initialize Dash app
app = dash.Dash(__name__)

# Create figure
fig = px.line(df, x="Year", y="GDP (USD)", title="GDP Over Time", markers=True)

# Layout
template = "plotly_dark"  # Change to "plotly" for a light theme
app.layout = html.Div([
    html.H1("Global Economic Dashboard", style={'textAlign': 'center'}),
    dcc.Graph(id="gdp-graph", figure=fig)
])

# Run server
if __name__ == "__main__":
    app.run(debug=True)  # Changed from app.run_server() to app.run()