import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import os
from app import app

# Mapbox token
mapbox_access_token = 'pk.eyJ1IjoiZGl5YW5haGFsaW0iLCJhIjoiY2txY2xxcjdjMDUzMjJ2cGh5YW00MDJmNyJ9.0r-bJmKlKME-hlz2Al67SA'

# Load dataset with only the required columns
# data_path = os.path.join(os.path.dirname(__file__), 'data/Clean Sexual Harassment NY.csv')

df = pd.read_csv("data/Clean Sexual Harassment NY.csv", usecols=['PD_DESC', 'Lat_Lon', 'HOUR', 'year', 'BORO_NM', 'PREM_TYP_DESC'])
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# csv_file_path = os.path.join(BASE_DIR, 'data', 'Clean Sexual Harassment NY.csv')

# Load the CSV file
# df = pd.read_csv(csv_file_path, usecols=['PD_DESC', 'Lat_Lon', 'HOUR', 'year', 'BORO_NM', 'PREM_TYP_DESC'])

# Define colors for the legend
legend_colors = {
    'CHILD SEXUAL ABUSE': 'Aqua',
    'SEXUAL ABUSE': 'Chartreuse',
    'SODOMY': 'DeepPink', 
    'SEXUAL MISCONDUCT': 'Gold',
    'OBSCENITY': 'Chocolate',
    'SEX OFFENSES': 'Olive',
    'INCEST': 'Crimson',
    'SEXUAL HARASSMENT': 'Fuchsia'
}
df['color'] = df['PD_DESC'].map(legend_colors)

# Split Lat_Lon into separate latitude and longitude columns
split_data = df.Lat_Lon.str.strip(')').str.strip('(').str.split(', ', expand=True)
df['lat'] = split_data[0].astype(float)  # Ensure lat and lon are float
df['lon'] = split_data[1].astype(float)

# Replace hour numbers with string labels
df['HOUR'] = df['HOUR'].replace({
    0: "12 am", 1: "1 am", 2: "2 am", 3: "3 am", 4: "4 am", 5: "5 am",
    6: "6 am", 7: "7 am", 8: "8 am", 9: "9 am", 10: "10 am", 11: "11 am",
    12: "12 pm", 13: "1 pm", 14: "2 pm", 15: "3 pm", 16: "4 pm", 17: "5 pm",
    18: "6 pm", 19: "7 pm", 20: "8 pm", 21: "9 pm", 22: "10 pm", 23: "11 pm"
})

# Define cards
card_main = dbc.Card(
    [
        dbc.CardBody(
            [
                html.P("Choose the year you would like to see on the map.", className="card-text"),
                dcc.Dropdown(
                    id='year',
                    multi=False,
                    clearable=True,
                    disabled=False,
                    value=2019,
                    placeholder='Select Year',
                    options=[{'label': i, 'value': i} for i in sorted(df['year'].unique())],
                    style={'display': True, 'backgroundColor': "#ffffff", 'width': '100%', 'height': '40px'}
                ),
                dcc.Graph(id='graph', style={"width": "100%", "height": "500px"})
            ]
        )
    ],
    color="light",
    inverse=False,
    outline=True,
    style={'height': '100vh'}
)

# Define the legend card
card_legend = dbc.Card(
    [
        dbc.CardBody(
            [
                html.Ul(
                    [
                        html.Li([
                            html.Span(style={'background-color': color, 'border-radius': '50%', 'display': 'inline-block',
                                             'width': '15px', 'height': '15px', 'margin-right': '5px'}),
                            label
                        ], style={'list-style-type': 'none', 'margin-bottom': '5px'})
                        for label, color in legend_colors.items()
                    ],
                    style={"margin-left": "-40px"}
                )
            ]
        )
    ],
    color="light",
    inverse=False,
    outline=True
)

card_boroughs = dbc.Card(
    [
        dbc.CardBody(
            [
                html.Label('Borough: ', style={'color': 'black', 'font-weight': 'bold', }),
                dbc.Checklist(
                    id='check_boroughs',
                    options=[{'label': str(b), 'value': b} for b in sorted(df['BORO_NM'].unique())],
                    value=[b for b in sorted(df['BORO_NM'].unique())],
                    labelCheckedStyle={"color": "green"}
                )
            ]
        )
    ],
    color="light",
    inverse=False,
    outline=True,
    style={"margin-left": "-70px"}
)

layout = html.Div([
    dbc.Row([dbc.Col(card_legend, width={"size": 3}),
             dbc.Col(card_boroughs, width={"size": 2}),
             dbc.Col(card_main, width={"size": 7})])
])

@app.callback(
    Output('graph', 'figure'),
    [Input('check_boroughs', 'value'),
     Input('year', 'value')]
)
def update_figure(chosen_boroughs, chosen_year):
    filtered_df = df[(df['BORO_NM'].isin(chosen_boroughs)) & (df['year'] == chosen_year)]

    if filtered_df.empty:
        return {
            'data': [],
            'layout': go.Layout(
                uirevision='foo',
                autosize=True,
                clickmode='event+select',
                hovermode='closest',
                margin=dict(t=0, b=0, l=0, r=0),
                hoverdistance=2,
                mapbox=dict(
                    accesstoken=mapbox_access_token,
                    bearing=25,
                    style='dark',
                    center=dict(lat=40.80105, lon=-73.945155),
                    zoom=10
                ),
            )
        }

    locations = [go.Scattermapbox(
        lon=filtered_df['lon'],
        lat=filtered_df['lat'],
        mode='markers',
        marker={'color': filtered_df['color']},
        unselected={'marker': {'opacity': 1}},
        selected={'marker': {'opacity': 0.5, 'size': 25}},
        text=filtered_df[['PD_DESC', 'HOUR', 'PREM_TYP_DESC']],
        hoverinfo='text'
    )]

    return {
        'data': locations,
        'layout': go.Layout(
            uirevision='foo',
            autosize=True,
            clickmode='event+select',
            hovermode='closest',
            margin=dict(t=0, b=0, l=0, r=0),
            hoverdistance=2,
            mapbox=dict(
                accesstoken=mapbox_access_token,
                bearing=25,
                style='dark',
                center=dict(lat=40.80105, lon=-73.945155),
                zoom=10
            ),
        )
    }

