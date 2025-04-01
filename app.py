import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

# Load GDP data
df = pd.read_csv("gdp_data.csv")

# Extract unique country names for dropdown
available_countries = df["Country"].unique()

# Initialize Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("🌍 Global GDP Dashboard", style={"textAlign": "center"}),

    # Dropdown for country selection
    dcc.Dropdown(
        id="country-selector",
        options=[{"label": country, "value": country} for country in available_countries],
        value="United States",  # Default value
        clearable=False
    ),

    # Graph
    dcc.Graph(id="gdp-graph"),
])

# Callback to update graph based on selected country
@app.callback(
    Output("gdp-graph", "figure"),
    Input("country-selector", "value")
)
def update_graph(selected_country):
    filtered_df = df[df["Country"] == selected_country]

    fig = px.line(
        filtered_df,
        x="Year",
        y="GDP (USD)",
        title=f"{selected_country} GDP Over Time",
        markers=True
    )
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="GDP (USD)",
        template="plotly_dark"  # You can change themes later
    )

    return fig

# Run the app
if __name__ == "__main__":
    app.run(debug=True)