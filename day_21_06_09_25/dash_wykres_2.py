from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from collections import deque
import random

app = Dash(__name__)

max_point = 20
times = deque(maxlen=max_point)
values = deque(maxlen=max_point)

times.append(1)
values.append(1)

app.layout = html.Div(
    [
        dcc.Graph(id="live-graph"),
        dcc.Interval(
            id="interval-component",
            interval=1000,
            n_intervals=0
        )
    ]
)

@app.callback(
    Output("live-graph", "figure"),
    Input('interval-component', "n_intervals")
)

def update_graph(n):
    times.append(times[-1] + 1)
    values.append(values[-1] + random.randint(-10, 10))

    fig = go.Figure(data=[go.Scatter(x=list(times), y=list(values), mode="lines+markers")])
    fig.update_layout(title="Dynamiczny wykres")
    return fig

if __name__ == '__main__':
    app.run(debug=True)