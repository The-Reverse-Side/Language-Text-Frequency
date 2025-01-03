from dash import Dash, html, dcc, Input, Output
import dash_daq as daq
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

df = pd.read_csv('./Output/OUTPUT_Spanish.csv')
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H4("Word Frequencies in Analyzed Text"),
                width={"size": 6, "offset": 3},  # Center the title
                style={"textAlign": "center", "marginTop": "20px"}
            )
        ),
        dbc.Row(
            dbc.Col(
                html.P("Select frequency threshold:"),
                width={"size": 6, "offset": 3},  # Center the slider label
                style={"textAlign": "center"}
            )
        ),
        dbc.Row(
            dbc.Col(
                dcc.Slider(
                    id="slider",
                    min=0,
                    max=df['Frequency'].max(),
                    step=5,
                    value=15,
                    tooltip={"always_visible": False, "style": {"color": "lightgrey", "fontSize": "20px"}},
                ),
                width={"size": 6, "offset": 3}  # Center the slider
            )
        ),
        dbc.Row(
            dbc.Col(
                dcc.Graph(id="graph"),
                width={"size": 10, "offset": 1},  # Center the graph
                style={"marginTop": "30px"}
            )
        ),
    ],
    fluid=True,  # Full-width container for responsiveness
    style={"padding": "20px"}  # Overall padding to avoid content touching edges
)

# Callback to update the graph based on the slider value
@app.callback(
    Output("graph", "figure"),
    Input("slider", "value")
)
def update_graph(value):
    dff = df.loc[df["Frequency"] >= value]
    fig = px.bar(dff, x="Word", y="Frequency", color="Frequency")
    fig.update_layout(title={"text": "Word Frequency Distribution", "x": 0.5, "xanchor": "center"})  # Center the title
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)