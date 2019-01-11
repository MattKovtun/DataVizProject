from dash import Dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go

import pandas as pd
from config import line_colors, text_colors

file = "twenty_one_pilots.csv"
df = pd.read_csv(file, skipinitialspace=True)

app = Dash(__name__)

top_songs = {"Trench": ["Jumpsuit", "My Blood", "Levitate", "Bandito", "Smithereens", "Cut My Lip"],
             "Vessel": ["Migraine", "Car Radio", "Guns for Hands"],
             "Blurryface": ["Heavydirtysoul", "Stressed Out", "Fairly Local", "Message Man", "Lane Boy",
                            "We Don't Believe What's on TV"]}

songs_positions = {"Trench": {"Jumpsuit": "bottom center", "My Blood": "bottom center", "Levitate": "top center",
                              "Bandito": "top center", "Smithereens": "bottom center", "Cut My Lip": "bottom center"},
                   "Blurryface": {"Heavydirtysoul": "top center", "Stressed Out": "bottom center",
                                  "Fairly Local": "top center", "Message Man": "bottom center",
                                  "Lane Boy": "top center", "We Don't Believe What's on TV": "top center"},
                   "Vessel": {}}


def create_scatter(album):
    return go.Scatter(
        x=df["Index"][df["Album"] == album],
        y=df["BPM"][df["Album"] == album],
        mode='lines+markers',
        line=dict(color=line_colors[album]),
        text=df["Song"][df["Album"] == album],
        name=album,
        hoverinfo='y+text'

    )


def create_texts(album, all=False):
    return go.Scatter(
        x=df["Index"][df["Album"] == album],
        y=df["BPM"][df["Album"] == album],
        mode='markers+text',
        line=dict(color=line_colors[album]),
        text=[song if song in top_songs[album] or all else None for song in df["Song"][df["Album"] == album]],
        textposition=[songs_positions[album][song] if song in songs_positions[album] else "top center" for song in
                      df["Song"][df["Album"] == album]],
        hoverinfo='none',
        showlegend=False,
        textfont=dict(
            family="Open Sans",
            size=15,
            color=text_colors[album]
        )
    )


def generate_graph():
    data = [create_scatter(album) for i, album in enumerate(df["Album"].unique()[1:])]
    [data.append(create_texts(album)) for i, album in enumerate(df["Album"].unique()[1:])]

    return {'data': data,
            'layout': go.Layout(
                yaxis=dict(range=[65, 185]),
                title='Розподіл останніх альбомів "twenty one pilots" за темпами',
                xaxis=dict(showline=False, showgrid=False, showticklabels=False)
            )}


def generate_secondary_graph():
    data = [create_scatter(df["Album"].unique()[0])]
    data.append(create_texts(df["Album"].unique()[0], True))
    return {'data': data,
            'layout': go.Layout(
                yaxis=dict(range=[65, 185]),
                title='',
                xaxis=dict(showline=False, showgrid=False, showticklabels=False)

            )}


app.layout = html.Div([
    dcc.Graph(id='graph',
              figure=generate_graph(),
              config={
                  'displayModeBar': False
              }),
    dcc.Graph(id='secondary-graph',
              figure=generate_secondary_graph(),
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
