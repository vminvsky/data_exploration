
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)

df = pd.read_csv("/ada1/projects/socialknowledge/src/webpage/data/article_reddit-wiki_partisan_scores_old.csv")


# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

fig = px.scatter(df, x="partisan_reddit", y="score", color="number_editors", hover_data=["page_title","GS"],
        labels=dict(partisan_reddit="Reddit partisan score", score="Wikipedia partisan score", number_editors="Number Editors"),height=600
    )

app.layout = html.Div(children=[
    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='scatter-plot',
        figure=fig
    ),
    html.P("Filter by number commenters:"),
    dcc.RangeSlider(
        id='range-slider',
        min=10, max=1000, step=5,
        marks={10: '10', 100: '100',1000: '1000'},
        value=[50, 300]
    ),
    html.P("Partisan-ness of article:"),
    dcc.RangeSlider(
        id='range-slider2',
        min=-3, max=3, step=0.01,
        marks={-1:"-1", 0: "0",1:"1"},
        value=[1,4]
    ),
    html.P("GS score:"),
    dcc.RangeSlider(
        id='range-slider3',
        min=.5, max=1, step=0.01,
        marks={0.5: ".5",1:"1"},
        value=[.5,1]
    ),
])

fig.update_yaxes(
    scaleanchor = "x",
    scaleratio = 1,
  )
@app.callback(
    Output("scatter-plot", "figure"), 
    [Input("range-slider", "value"),
    Input("range-slider2", "value"),
    Input("range-slider3", "value")])
def update_bar_chart(slider_range,slider_range2,slider_range3):
    df = pd.read_csv("/ada1/projects/socialknowledge/src/webpage/data/article_reddit-wiki_partisan_scores_old.csv")
    low, high = slider_range
    low2,high2=slider_range2
    low3,high3=slider_range3

    mask = (df['number_commenters'] > low) & (df['number_commenters'] < high)& (df['partisan_neutral'] < high2) & (df['partisan_neutral'] > low2) & (df['GS'] < high3) & (df['GS'] > low3) 
    fig = px.scatter(
        df[mask], x="partisan_reddit", y="score", color="number_editors",
        hover_data=['page_title',"GS"],
        labels=dict(partisan_reddit="Reddit partisan score", score="Wikipedia partisan score", number_editors="Number Editors"), height = 600)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)



