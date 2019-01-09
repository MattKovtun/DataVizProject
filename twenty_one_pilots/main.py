from dash import Dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go

import pandas as pd
from config import line_colors

file = "twenty_one_pilots.csv"
df = pd.read_csv(file, skipinitialspace=True)

app = Dash(__name__)
# for i, album in enumerate(df["Album"].unique()):
#     print(df["Song"][df["Album"] == album].values)

def generate_graph():
    return {'data':
        [
            go.Scatter(
                x=df["Index"][df["Album"] == album],
                y=df["BPM"][df["Album"] == album],
                mode='lines+markers',
                line=dict(color=line_colors[i]),
                name=album

            ) for i, album in enumerate(df["Album"].unique())

        ],
        'layout': go.Layout(
            # annotations=[
            #     dict(
            #         x=5,
            #         y=85,
            #         xref='x',
            #         yref='y',
            #         text='max=5',
            #
            #         font=dict(
            #             family='Courier New, monospace',
            #             size=16,
            #             color='#ffffff'
            #         ),
            #         align='center',
            #         arrowhead=2,
            #         arrowsize=1,
            #         arrowwidth=2,
            #         arrowcolor='#636363',
            #         ax=20,
            #         ay=-30,
            #         bordercolor='#c7c7c7',
            #         borderwidth=2,
            #         borderpad=4,
            #         bgcolor='#ff7f0e',
            #         opacity=0.8
            #     )
            # ]
        )}


app.layout = html.Div([
    dcc.Graph(id='graph', figure=generate_graph())
],
    style={"max-width": "1140px",
           "margin": "auto",
           "height": "800px"}
)

if __name__ == "__main__":
    app.run_server(debug=True)
