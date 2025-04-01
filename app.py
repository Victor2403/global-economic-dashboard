import dash
from dash import dcc, html  # Correct modern imports
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

# Load GDP data
df = pd.read_csv("gdp_data.csv")

# List of unique countries
countries = df["Country"].unique()

# Initialize Dash app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div(
    style={"backgroundColor": "#f4f4f4", "padding": "20px"},
    children=[
        html.H1(
            "Global GDP Dashboard",
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
                    value="United States",
                    style={
                        "width": "50%",
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
        dcc.Graph(id="gdp-graph"),
    ],
)

# Define callback
@app.callback(
    Output("gdp-graph", "figure"),
    Input("country-dropdown", "value")  # Simplified input syntax (no list needed)
)
def update_graph(selected_country):
    filtered_df = df[df["Country"] == selected_country]
    
    figure = {
        "data": [
            go.Scatter(
                x=filtered_df["Year"],
                y=filtered_df["GDP (USD)"],
                mode="lines+markers",
                line={"color": "#00cc66", "width": 3},
                marker={"size": 8, "color": "white", "line": {"color": "#00cc66", "width": 2}},
            )
        ],
        "layout": go.Layout(
            title=f"GDP of {selected_country} Over Time",
            plot_bgcolor="#f4f4f4",
            paper_bgcolor="#f4f4f4",
            xaxis={"title": "Year", "gridcolor": "#d3d3d3"},
            yaxis={"title": "GDP (USD)", "gridcolor": "#d3d3d3"},
        ),
    }
    return figure

if __name__ == "__main__":
    app.run(debug=True)