from dash import html, dcc
import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go

from app import app_dash

# Step 2. Import the dataset, only loading required columns
df = pd.read_csv("src/data/Clean Sexual Harassment NY.csv", usecols=['year', 'PD_DESC', 'CMPLNT_NUM', 'BORO_NM'])

# Filter data to include only the years of interest
years_of_interest = [1997, 1999, 2001, 2003, 2005, 2007, 2009, 2011, 2013, 2015, 2017, 2019]
df = df[df['year'].isin(years_of_interest)]

card_1 = dbc.Card(
                [
                    dbc.CardHeader(""),
                    dbc.CardBody(
                        html.H2(className="card-title"),
                    ),
                ],
                id="card_1",
                className="text-center mb-2",
                color="light",
                style={
                    "color": "YellowGreen",},
                outline=True
)
card_2 = dbc.Card(
                [
                    dbc.CardHeader(""),
                    dbc.CardBody(
                        html.H2(className="card-title"),
                    ),
                ],
                id="card_2",
                className="text-center mb-2",
                color="light",
                style={
                    "color": "YellowGreen",},
                outline=True
)
card_3 = dbc.Card(
                [
                    dbc.CardHeader(""),
                    dbc.CardBody(
                        html.H2(className="card-title"),
                    ),
                ],
                id="card_3",
                className="text-center mb-2",
                color="light",
                style={
                    "color": "YellowGreen",},
                outline=True
)

layout = html.Div([
    
        dbc.Row(
        [dbc.Col(dcc.Slider(
        id='app-1-year-slider',
        min=min(years_of_interest),
        max=max(years_of_interest),
        value=min(years_of_interest),
        step=2,  # Adjusted step to 2 to skip to every second year in our list
        marks={year: str(year) for year in years_of_interest},
        className="year-slider")), 
    ],
        
    ),
    dbc.Row([dbc.Col(card_1, width={"size": 3, "offset": 1}), dbc.Col(card_2, width=3), dbc.Col(card_3, width=3) ]),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id='hbar'),
                        lg={'size': 6,  "offset": 0, 'order': 'first'}
                        ),
                dbc.Col(dcc.Graph(id='piechart'),
                        lg={'size': 6,  "offset": 0, 'order': 'last'}
                        ),
            ]
        )

])

@app_dash.callback(
    [Output('card_1', 'children'), Output('card_2', 'children'), Output('card_3', 'children'), Output('hbar','figure'), Output('piechart','figure')],
    [Input('app-1-year-slider', 'value')])
def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]
    cpd_desc = filtered_df.groupby(["PD_DESC"])['CMPLNT_NUM'].size().to_frame('Count').reset_index()
    highest_sex_type = cpd_desc['PD_DESC'][cpd_desc.Count == cpd_desc['Count'].max()]

    card_1 = dbc.Card(
                [
                    dbc.CardHeader(html.H5("Top Sex Crime in " + str(selected_year))),
                    dbc.CardBody(
                        html.H3(highest_sex_type, className="card-title", id="card-title"),
                    ),
                ],
                className="text-center mb-2",
                color="light",
                style={"backgroundColor": "LightBlue",
                    "color": "DarkCyan",},
                outline=True
    )
    numOfRows = len(filtered_df.index)
    card_2 = dbc.Card(
                [
                    dbc.CardHeader(html.H5("Total Cases in " + str(selected_year))),
                    dbc.CardBody(
                        html.H3(numOfRows, className="card-title", id="card-title"),
                    ),
                ],
                className="text-center mb-2",
                color="light",
                style={"backgroundColor": "LightSkyBlue",
                    "color": "DarkCyan",},
                outline=True
    )
    cboro_nm = filtered_df.groupby(["BORO_NM"])['CMPLNT_NUM'].size().to_frame('Count').reset_index()
    highest_boro = cboro_nm['BORO_NM'][cboro_nm.Count == cboro_nm['Count'].max()]
    card_3 = dbc.Card(
                [
                    dbc.CardHeader(html.H5("Hot Spot in " + str(selected_year))),
                    dbc.CardBody(
                        html.H3(highest_boro, className="card-title", id="card-title"),
                    ),
                ],
                className="text-center mb-2",
                color="light",
                style={"backgroundColor": "LightCyan",
                    "color": "DarkCyan",},
                outline=True
    )

    y = cpd_desc['PD_DESC'].to_list()
    x = cpd_desc['Count'].to_list()
    fig1 = go.Figure(data=[go.Bar(x=x, 
                  y=y,
                  orientation='h',
                  marker=dict(color='aquamarine')
                  )])
    fig1.update_layout(
        xaxis=dict(
        showgrid=False,
    ),
    yaxis=dict(
        showgrid=False,
    ),
    paper_bgcolor='AliceBlue',
    plot_bgcolor='AliceBlue',
    margin=dict(t=70, b=70, l=70, r=70),
    showlegend=False,
    height=400,
    title_text="Total Cases By Categories",
    title_x=0.5,
    font=dict(
        family="Courier New, monospace",
        size=12,
        ),
    )

    labels = cboro_nm['BORO_NM'].to_list()
    values = cboro_nm['Count'].to_list()
    colors = ['palegreen', 'paleturquoise', 'papayawhip', 'pink', 'plum']

    fig2 = go.Figure(data=[go.Pie(labels=labels, values=values, marker=dict(colors=colors))])
    fig2.update_layout(
    paper_bgcolor='AliceBlue',
    plot_bgcolor='AliceBlue',
    margin=dict(t=70, b=70, l=70, r=70),
    showlegend=True,
    height=400,
    title_text="Total Cases By Boroughs",
    title_x=0.5,
    font=dict(
        family="Courier New, monospace",
        size=12,
        ),
    )
    return card_1, card_2, card_3, fig1, fig2