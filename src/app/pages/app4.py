from dash import dcc, html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import os

from app import app_dash

# Import the dataset with the necessary columns
# Construct path relative to the src directory
# data_path = os.path.join(os.path.dirname(__file__), 'data/Clean Sexual Harassment NY.csv')
df = pd.read_csv("src/data/Clean Sexual Harassment NY.csv", usecols=['LOC_OF_OCCUR_DESC', 'HOUR', 'year', 'CMPLNT_NUM', 'PREM_TYP_DESC'])
df.columns = [col.strip() for col in list(df.columns)]

df['Location'] = df['LOC_OF_OCCUR_DESC']
df['period'] = (df['HOUR'] % 24 + 4) // 4
df['period'].replace({1: 'Late Night',
                      2: 'Early Morning',
                      3: 'Morning',
                      4: 'Noon',
                      5: 'Evening',
                      6: 'Night'}, inplace=True)

# Divide 'period' into 2 times: Day and Night
df.loc[df['period'].str.contains('Night'), 'period'] = 'Night'
df.loc[df['period'].str.contains('Morning'), 'period'] = 'Day'
df['period'] = df['period'].replace({'Evening': 'Night'}, regex=True)
df['period'] = df['period'].replace({'Noon': 'Day'}, regex=True)

df.sort_values('HOUR', inplace=True)
df['HOUR'] = df['HOUR'].replace({0: "12 am", 1: "1 am", 2: "2 am", 3: "3 am", 4: "4 am", 5: "5 am", 6: "6 am", 7: "7 am", 8: "8 am",
                                9: "9 am", 10: "10 am", 11: "11 am", 12: "12 pm", 13: "1 pm", 14: "2 pm", 15: "3 pm", 16: "4 pm", 17: "5 pm",
                                18: "6 pm", 19: "7 pm", 20: "8 pm", 21: "9 pm", 22: "10 pm", 23: "11 pm"})
df['Location'] = df['Location'].replace({"PUBLIC": "Public", "INSIDE": "Inside"})

# Layout for time variation page
card_morning = dbc.Card(
    [
        dbc.CardBody(
            html.H2(className="card-title"),
        ),
        dbc.CardImg(
            src="/assets/images/morning.png",
            bottom=True,
        ),
    ],
    id="card_morning",
    className="text-center mb-2",
    color="light",
    style={"color": "YellowGreen", "border": "none", "width": "15rem"},
    outline=True
)

card_night = dbc.Card(
    [
        dbc.CardBody(
            html.H2(className="card-title"),
        ),
        dbc.CardImg(
            src="/assets/images/night.png",
            bottom=True
        ),
    ],
    id="card_night",
    color="light",
    outline=True,
    className="text-center mb-2",
    style={"color": "YellowGreen", "border": "none", "width": "15rem"}
)

card_year = dbc.Card(
    [
        dbc.CardBody(
            [
                html.P(
                    "Choose the year you would like to see on the line chart.",
                    className="card-text",
                ),
                dcc.Dropdown(
                    id='select_year',
                    multi=False,
                    clearable=True,
                    disabled=False,
                    value=2019,
                    placeholder='Select Year',
                    options=[{'label': s, 'value': s} for s in sorted(df.year.unique())],
                ),
                html.Br(),
                html.P(
                    "Click on one of the options to discover more.",
                    className="card-text",
                ),
                dbc.CardGroup([
                    dbc.RadioItems(
                        options=[],
                        id="select_location",
                        inline=True,
                    ),
                ])
            ]
        ),
    ],
    color="light",
    inverse=False,
    outline=False,
)

table = dbc.Table(
    id="table_1",
)

layout = html.Div([
    dbc.Row([dbc.Col(card_morning, width="auto"), 
             dbc.Col(card_night, width="auto"), 
             dbc.Col(card_year, width="auto", align="center")], justify="evenly"),
    dbc.Row([dbc.Col(dcc.Graph(id='line_chart1'), lg={'size': 8, "offset": 0, 'order': 'first'}), 
             dbc.Col(table)])
])

@app_dash.callback(
    [Output("card_morning", "children"), 
     Output("card_night", "children"), 
     Output("line_chart1", "figure"), 
     Output("select_location", "options")],
    Input("select_year", "value")
)
def update_layout(selected_year):
    filtered_df = df[df.year == selected_year]

    cperiod = filtered_df['period'].value_counts().to_frame()
    cperiod.reset_index(inplace=True)
    cperiod.columns = ['period', 'count']

    # First card
    card_1 = dbc.Card(
        [
            dbc.CardBody(
                html.H2(cperiod[cperiod['period'] == 'Day']['count'].values[0], className="card-title"),
            ),
            dbc.CardImg(
                src="/assets/images/morning.png",
                bottom=True,
                style={"width": "100%", "height": "100%", "object-fit": "cover", "border-radius": "20px"},
                className="card border-end-0 border-top-0 border-bottom-0 border-5 shadow-lg",
            ),
        ],
        className="text-center",
        color="light",
        style={"color": "YellowGreen", "border": "none"},
        outline=True,
    )

    # Second card
    card_2 = dbc.Card(
        [
            dbc.CardBody(
                html.H2(cperiod[cperiod['period'] == 'Night']['count'].values[0], className="card-title"),
            ),
            dbc.CardImg(
                src="/assets/images/night.png",
                bottom=True,
                style={"width": "100%", "height": "100%", "object-fit": "cover", "border-radius": "20px"},
                className="card border-end-0 border-top-0 border-bottom-0 border-5 shadow-lg",
            ),
        ],
        color="light",
        outline=True,
        className="text-center mb-2",
        style={"color": "YellowGreen", "border": "none"}
    )

    filtered_df['Total Cases'] = filtered_df.groupby(['HOUR', 'Location']).CMPLNT_NUM.transform('count')
    # Display multi-line chart
    fig6 = px.line(filtered_df, x='HOUR', y='Total Cases', color='Location')
    fig6.update_layout(
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        paper_bgcolor='hsl(120, 60%, 95%)',
        plot_bgcolor='hsl(120, 60%, 95%)',
        showlegend=True,
        height=332,
        title_text="Variation of Time",
        title_x=0.5,
        font=dict(
            family="Courier New, monospace",
            size=12
        )
    )
    location_of_year = [{'label': c, 'value': c} for c in sorted(filtered_df.Location.unique())]

    return card_1, card_2, fig6, location_of_year

@app_dash.callback(
    Output('table_1', 'children'),
    [Input('select_year', 'value')],
    [Input('select_location', 'value')],
    prevent_initial_call=True
)
def update_table(selected_year, selected_location):
    filtered_df = df[df.year == selected_year]
    filtered_df = filtered_df[filtered_df['Location'] == selected_location]
    df_new = filtered_df.groupby('PREM_TYP_DESC').size().reset_index(name='Total Cases')
    df_new = df_new.sort_values('Total Cases', ascending=False)
    table = dbc.Table.from_dataframe(df_new, 
                                     striped=True, 
                                     bordered=True, 
                                     hover=True, 
                                     size='md', 
                                     responsive='sm',
                                     color='primary',
                                     style={
                                         "text-align": "center", 
                                         "height": "332px", 
                                         "display": "block",
                                         "overflowY": "scroll", 
                                         "overflowX": "auto"
                                         })
    return table
