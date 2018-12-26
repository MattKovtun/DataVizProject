from dash import Dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import pandas as pd

from main import select_specifics

app = Dash(__name__)

filename = "music.csv"
df = select_specifics(filename)
df = df.loc[~(df == 0).any(axis=1)]
# df = df.dropna() # if want to use 'hottest'


def select_by_vals(vals, ddf):
    cond = (ddf["terms"] == vals[0])
    for cat in vals[1:]:
        cond |= (ddf["terms"] == cat)
    return cond


def bin_data(ddf):
    data = []
    bins = [i for i in range(40, 231, 10)]
    labels = [str(i) for i in bins[:-1]]
    for term in ddf["terms"].unique():
        cond = select_by_vals([term], ddf)
        binned = pd.cut(ddf[cond]['tempo'], bins=bins, labels=labels)
        data.append(ddf[cond].groupby(binned).size())

    return data


def generate_graph():
    vals = ["latin jazz", "hip hop", "blues-rock"]

    cond = select_by_vals(vals, df)

    ddf = df[cond]
    ddf = ddf.sort_values("tempo", ascending=True)


    binned = bin_data(ddf)

    return {'data':
        [
            go.Scatter(
                x=list(binned[t].keys()),
                y=list(binned[t]),
                name=ddf['terms'].unique()[t],
                fill='tozeroy',
                mode='lines'
            ) for t in range(len(binned))

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
