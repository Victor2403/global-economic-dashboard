import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

# Load economic data
df = pd.read_csv("economic_data.csv")

# List of unique countries
countries = df["Country"].unique()

# Initialize Dash app
app = dash.Dash(__name__)

# Define layout
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
            ],
            style={"fontSize": "18px"},
        ),
        html.Div(id="graph-container"),
    ],
)

# Define callback
@app.callback(
    Output("graph-container", "children"),
    [Input("country-dropdown", "value"), Input("tabs", "value")],
)
def update_graph(selected_countries, selected_tab):
    if not selected_countries:
        return html.Div("⚠️ Please select at least one country.", style={"color": "red", "fontSize": "20px"})

    metric_mapping = {
        "gdp": ("GDP (USD)", "GDP Over Time", "#00cc66"),
        "inflation": ("Inflation (%)", "Inflation Rate Over Time", "#ff6600"),
        "unemployment": ("Unemployment (%)", "Unemployment Rate Over Time", "#3366cc"),
    }
    metric, title, color = metric_mapping[selected_tab]

    traces = []
    for country in selected_countries:
        filtered_df = df[df["Country"] == country]
        traces.append(
            go.Scatter(
                x=filtered_df["Year"],
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


if __name__ == "__main__":
    app.run(debug=True)