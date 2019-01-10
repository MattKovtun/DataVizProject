from dash import Dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go

import pandas as pd
from config import line_colors, text_colors

file = "twenty_one_pilots.csv"
df = pd.read_csv(file, skipinitialspace=True)

app = Dash(__name__)

top_songs = {"Trench": ["Jumpsuit", "My Blood", "Neon Gravestones"],
             "Vessel": ["Migraine", "Car Radio", "Guns for Hands"],
             "Blurryface": ["Heavydirtysoul", "Stressed Out", "Tear in My Heart"]}


def generate_graph():
    data = [
        go.Scatter(
            x=df["Index"][df["Album"] == album],
            y=df["BPM"][df["Album"] == album],
            mode='lines+markers',
            line=dict(color=line_colors[i]),
            text=df["Song"][df["Album"] == album],
            name=album,
            hoverinfo='y+text'

        ) for i, album in enumerate(df["Album"].unique())
    ]
    [data.append(
        go.Scatter(
            x=df["Index"][df["Album"] == album],
            y=df["BPM"][df["Album"] == album],
            mode='markers+text',
            line=dict(color=line_colors[i]),
            text=[song if song in top_songs[album] else None for song in df["Song"][df["Album"] == album]],
            textposition="top center",
            hoverinfo='none',
            showlegend=False,
            textfont=dict(
                family="Open Sans",
                size=15,
                color=text_colors[i]
            )
        )
    ) for i, album in enumerate(df["Album"].unique())]

    return {'data': data,
            'layout': go.Layout(
                yaxis=dict(range=[65, 185]),
                title='Розподіл останніх альбомів "twenty one pilots" за темпами'
            )}


app.layout = html.Div([
    dcc.Graph(id='graph',
              figure=generate_graph(),
              config={
                  'displayModeBar': False
              })
],
    style={"max-width": "1140px",
           "margin": "auto",
           "height": "800px"}
)

if __name__ == "__main__":
    app.run_server(debug=True, port=8080, host='0.0.0.0')
