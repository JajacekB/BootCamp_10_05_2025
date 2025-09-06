from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd

df = pd.DataFrame({
    "Miasto": ["Warszaw", "Kraków", "Gliwic", "Łódź"],
    "Populacja": [1790658, 779115, 169750, 655345]
})

fig = px.bar(df, x='Miasto', y="Populacja", title="Populacja polskich mist")

app = Dash(__name__)

app.layout = html.Div(
    [html.H1("Dashboard z Dash i Ploty"),
     dcc.Graph(id="bar=chart", figure=fig)
     ]
)

if __name__ == '__main__':
    app.run(debug=True)