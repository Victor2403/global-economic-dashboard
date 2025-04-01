import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("gdp_data.csv")

# Get unique countries
countries = df["Country"].unique()

# Initialize app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Global GDP Dashboard", style={'textAlign': 'center'}),
    
    # Dropdown for country selection
    html.Label("Select a country:"),
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': country, 'value': country} for country in countries],
        value='United States',
        clearable=False
    ),
    
    # Line chart
    dcc.Graph(id='gdp-line-chart'),
    
    # Bar chart
    dcc.Graph(id='gdp-bar-chart')
])

# Callbacks for interactivity
@app.callback(
    [Output('gdp-line-chart', 'figure'), Output('gdp-bar-chart', 'figure')],
    [Input('country-dropdown', 'value')]
)
def update_graphs(selected_country):
    filtered_df = df[df['Country'] == selected_country]
    
    line_fig = px.line(
        filtered_df, x='Year', y='GDP (USD)', 
        title=f"GDP Growth of {selected_country}", markers=True
    )
    
    bar_fig = px.bar(
        filtered_df, x='Year', y='GDP (USD)', 
        title=f"Yearly GDP of {selected_country}"
    )
    
    return line_fig, bar_fig

if __name__ == "__main__":
    app.run(debug=True)