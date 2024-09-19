from dash import dcc, html
import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import os

from app import app

# Import the dataset with only the necessary columns
# Construct path relative to the src directory
# data_path = os.path.join(os.path.dirname(__file__), 'data/Clean Sexual Harassment NY.csv')
# df = pd.read_csv("data/Clean Sexual Harassment NY.csv", usecols=['year', 'suspector_sex_rand', 'suspector_age_rand', 'CMPLNT_NUM'])
# Get the absolute path to the project root directory (one level up from the current file)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
csv_file_path = os.path.join(project_root, 'data', 'Clean Sexual Harassment NY.csv')

# Load the CSV file
df = pd.read_csv(csv_file_path, usecols=['year', 'suspector_sex_rand', 'suspector_age_rand', 'CMPLNT_NUM'])

# Copy columns to new columns with clearer names
df['Year'] = df['year']

# Copy columns to new columns with clearer names
df['Year'] = df['year']
df['suspector_sex_rand'] = df['suspector_sex_rand'].replace({"F": "Female", "M": "Male"})

# Calculate total victims and percentages
total_victims = len(df.index)
total_female = len(df[df['suspector_sex_rand'] == "Female"])
total_male = len(df[df['suspector_sex_rand'] == "Male"])

female_percentage = round((total_female / total_victims) * 100)
male_percentage = round((total_male / total_victims) * 100)

card_main = dbc.Card(
    [
        dbc.CardBody(
            [
                html.P(
                    "Choose the year you would like to see on the bar chart.",
                    className="card-text",
                ),
                dcc.Dropdown(
                    id='year',
                    multi=False,
                    clearable=True,
                    disabled=False,
                    value=2019,
                    placeholder='Select Year',
                    options=sorted([{'label': i, 'value': i}
                                    for i in df['year'].unique()], key=lambda x: x['label']),
                ),
            ]
        ),
    ],
    color="light",
    inverse=False,
    outline=False,
)

card_warning = dbc.Card(
    [
        dbc.CardImg(src="/assets/images/warning.gif", bottom=True),
        dbc.CardBody([]),
    ],
    color="light",
    inverse=False,
    outline=True,
    className="text-center mb-2",
    style={
        "width": "15rem",
        "border": "none"
    }
)

card_sus_female = dbc.Card(
    [
        dbc.CardBody(
            html.H2(className="card-title"),
        ),
        dbc.CardImg(
            src="/assets/images/female.gif",
            bottom=True
        ),
    ],
    id="card_sus_female",
    color="light",
    outline=True,
    style={"width": "18rem", "margin-bottom": "1rem", "border": "none"}
)

card_sus_male = dbc.Card(
    [
        dbc.CardBody(
            html.H2(className="card-title"),
        ),
        dbc.CardImg(
            src="/assets/images/male.gif",
            bottom=True
        ),
    ],
    id="card_sus_male",
    color="light",
    outline=True,
    style={"width": "18rem", "margin-bottom": "1rem", "border": "none"}
)

layout = html.Div([
    dbc.Row([dbc.Col(card_sus_female, width="auto"), 
             dbc.Col(card_warning, width="auto", align="end"), 
             dbc.Col(card_sus_male, width="auto"),
             dbc.Col(card_main, width="auto")], justify="center"),
    dbc.Row([dcc.Graph(id="line_chart3")])
])

@app.callback(
    [Output("card_sus_female", "children"),
     Output("card_sus_male", "children"),
     Output("line_chart3", "figure")],
    [Input("year", "value")]
)
def update_figure(year_chosen):
    filtered_df = df[df['Year'] == year_chosen]
    gender = ['Female', 'Male']
    new_df = filtered_df.groupby(["suspector_age_rand", "suspector_sex_rand"])['CMPLNT_NUM'].size().to_frame('Count').reset_index()

    card_suspect_female = dbc.Card(
        [
            dbc.CardBody(
                html.H2(new_df[new_df.suspector_sex_rand == 'Female'].Count.sum(), className="card-title"),
            ),
            dbc.CardImg(
                src="/assets/images/female.gif",
                bottom=True,
                style={"width": "100%", "height": "100%", "object-fit": "cover", "border-radius": "20px"}, 
                className="card border-end-0 border-top-0 border-bottom-0 border-5 shadow-lg",
            ),
        ],
        color="light",
        outline=True,
        className="text-center mb-2",
        style={
            "color": "PaleVioletRed",
            "border": "none"
        }
    )

    card_suspect_male = dbc.Card(
        [
            dbc.CardBody(
                html.H2(new_df[new_df.suspector_sex_rand == 'Male'].Count.sum(), className="card-title"),
            ),
            dbc.CardImg(
                src="/assets/images/male.gif",
                bottom=True,
                style={"width": "100%", "height": "100%", "object-fit": "cover", "border-radius": "20px"}, 
                className="card border-end-0 border-top-0 border-bottom-0 border-5 shadow-lg",
            ),
        ],
        color="light",
        outline=True,
        className="text-center mb-2",
        style={
            "color": "PaleVioletRed",
            "border": "none"
        }
    )

    fig8 = go.Figure()
    fig8.add_trace(go.Bar(
        x=gender,
        y=new_df[new_df['suspector_age_rand'] == "<18"]["Count"].to_list(),
        name='Under 18',
        marker_color='DeepPink'
    ))
    fig8.add_trace(go.Bar(
        x=gender,
        y=new_df[new_df['suspector_age_rand'] == "18-24"]["Count"].to_list(),
        name='Between 18 and 24',
        marker_color='HotPink'
    ))
    fig8.add_trace(go.Bar(
        x=gender,
        y=new_df[new_df['suspector_age_rand'] == "25-44"]["Count"].to_list(),
        name='Between 25 and 44',
        marker_color='LightPink'
    ))
    fig8.add_trace(go.Bar(
        x=gender,
        y=new_df[new_df['suspector_age_rand'] == "45-64"]["Count"].to_list(),
        name='Between 45 and 64',
        marker_color='PaleVioletRed'
    ))
    fig8.add_trace(go.Bar(
        x=gender,
        y=new_df[new_df['suspector_age_rand'] == "65+"]["Count"].to_list(),
        name='Above 65',
        marker_color='LightCoral'
    ))

    fig8.update_layout(
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15,
        bargroupgap=0.1,
        paper_bgcolor='LavenderBlush',
        plot_bgcolor='LavenderBlush',
        autosize=True,
        margin=dict(t=0, b=0, l=0, r=0),
        height=374,
        title_x=0.5,
        font=dict(
            family="Courier New, monospace",
            size=12
        )
    )

    return card_suspect_female, card_suspect_male, fig8