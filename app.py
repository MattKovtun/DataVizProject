from dash import Dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go

from main import select_specifics

app = Dash(__name__)

filename = "music.csv"
df = select_specifics(filename)


def generate_graph():
    # print(df["tempo"])
    # print(df["song.hotttnesss"])
    ddf = df.loc[~(df == 0).any(axis=1)]
    ddf = ddf.dropna()

    categories = ["latin jazz", "hip hop", "blues-rock"]

    cond = (ddf["terms"] == categories[0])
    for cat in categories[1:]:
        cond |= (ddf["terms"] == cat)

    ddf = ddf[cond].sort_values("tempo", ascending=True)

    # print(ddf[ddf["terms"] == "hip hop"]["tempo"].tolist())


    colors = ["red", "green", "blue"]

    return {'data':
        [
            go.Scatter(
                x=ddf[ddf["terms"] == term]["tempo"],
                y=ddf[ddf["terms"] == term]["song.hotttnesss"],
                text=ddf[ddf["terms"] == term]["artist.name"],
                mode='lines',
                name=term
            ) for term in ddf["terms"].unique()

        ],
        'layout': go.Layout()}


app.layout = html.Div([
    dcc.Graph(id='graph', figure=generate_graph())
],
    style={"max-width": "1140px",
           "margin": "auto",
           "height": "800px"}
)

if __name__ == "__main__":
    app.run_server(debug=True)
