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

vals = ("latin jazz", "hip hop", "blues-rock", "ccm")
alpha = 0.2
fill_colors = ("rgba(238, 82, 83, %s)" % alpha,
               "rgba(52, 31, 151, %s)" % alpha,
               "rgba(131, 149, 167,%s)" % alpha,
               "rgba(99, 110, 114, %s)" % alpha)

alpha *= 4
line_colors = ("rgba(238, 82, 83, %s)" % alpha,
               "rgba(52, 31, 151, %s)" % alpha,
               "rgba(131, 149, 167,%s)" % alpha,
               "rgba(99, 110, 114, %s)" % alpha)


# df = df.loc[~(df == 0).any(axis=1)]
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
    for term in vals:
        cond = select_by_vals([term], ddf)
        binned = pd.cut(ddf[cond]['tempo'], bins=bins, labels=labels)
        data.append(ddf[cond].groupby(binned).size())

    return data


def generate_graph():
    cond = select_by_vals(vals, df)

    ddf = df[cond]
    ddf = ddf.sort_values("tempo", ascending=True)

    binned = bin_data(ddf)

    return {'data':
        [
            go.Scatter(
                x=list(binned[t].keys()),
                y=list(binned[t]),
                name=vals[t],
                fill='tozeroy',
                mode='lines',
                line=dict(color=line_colors[t]),
                fillcolor=fill_colors[t]
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
