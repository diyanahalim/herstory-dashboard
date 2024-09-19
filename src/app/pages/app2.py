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
# df = pd.read_csv("data/Clean Sexual Harassment NY.csv", usecols=['year', 'victim_sex_rand', 'victim_age_rand', 'CMPLNT_NUM'])
# Get the absolute path to the project root directory (one level up from src/app)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
csv_file_path = os.path.join(project_root, 'data', 'Clean Sexual Harassment NY.csv')

# Load the CSV file
df = pd.read_csv(csv_file_path, usecols=['year', 'victim_sex_rand', 'victim_age_rand', 'CMPLNT_NUM'])

# Prepare the DataFrame
df['Year'] = df['year']
df['victim_sex_rand'] = df['victim_sex_rand'].replace({"F": "Female", "M": "Male"})

# Calculate totals
total_victims = len(df.index)
total_female = len(df[df['victim_sex_rand'] == "Female"])
total_male = len(df[df['victim_sex_rand'] == "Male"])

# Calculate percentages
female_percentage = round((total_female / total_victims) * 100)
male_percentage = round((total_male / total_victims) * 100)

# Define cards
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
    outline=False,
)

card_vic_female = dbc.Card(
    [
        dbc.CardBody(
            html.H2(className="card-title")
        ),
        dbc.CardImg(src="/assets/images/female.gif", bottom=True, alt="Female gif"),
    ],
    id="card_vic_female",
    color="light",
    outline=True,
    style={
        "width": "18rem",
        "margin-bottom": "1rem",
        "border": "none",
    }
)

card_vic_total = dbc.Card(
    [
        dbc.CardHeader("Total Victims"),
        dbc.CardBody(
            html.H1(className="card-title"),
        ),
    ],
    id="card_vic_total",
    outline=False,
    className="text-center mb-15",
    style={
        "color": "RebeccaPurple",
        "font-size": "20px",
        # "margin-right": "4rem",
        "backgroundColor": "Plum"
    }
)

card_vic_male = dbc.Card(
    [
        dbc.CardBody(
            html.H2(className="card-title"),
        ),
        dbc.CardImg(src="/assets/images/male.gif", bottom=True, alt="Male gif"),
    ],
    id="card_vic_male",
    color="light",
    outline=True,
    style={
        "width": "18rem",
        "margin-bottom": "1rem",
        "border": "none",
    }
)

layout = html.Div([
    dbc.Row([dbc.Col(card_vic_female, width="auto"), dbc.Col(card_vic_total, width="auto", align="center"), dbc.Col(card_vic_male, width="auto"), dbc.Col(card_main, width="auto")], justify="center"),
    dbc.Row([dcc.Graph(id='line_chart2')])
])

@app.callback(
    [Output("card_vic_female", "children"),
     Output("card_vic_total", "children"),
     Output("card_vic_male", "children"),
     Output("line_chart2", "figure")],
    [Input("year", "value")]
)
def update_figure(year_chosen):
    if year_chosen not in df['Year'].values:
        return (
    dbc.Card([dbc.CardBody(html.H2("No data available"))]),
    dbc.Card([dbc.CardBody(html.H1("0"))]),
    dbc.Card([dbc.CardBody(html.H2("0"))]),
    go.Figure()
)

    filtered_df = df[df['Year'] == year_chosen]
    
    new_df = filtered_df.groupby(["victim_age_rand", "victim_sex_rand"])['CMPLNT_NUM'].size().to_frame('Count').reset_index()
    
    card_victim_female = dbc.Card(
        [
            dbc.CardBody(
                html.H2(new_df[new_df.victim_sex_rand == 'Female'].Count.sum(), className="card-title"),
            ),
            dbc.CardImg(src="/assets/images/female.gif", bottom=True, alt="Female gif", style={"width": "100%", "height": "100%", "object-fit": "cover", "border-radius": "20px"}, className="card border-end-0 border-top-0 border-bottom-0 border-5 shadow-lg",),
        ],
        className="text-center mb-2",
        color="light",
        outline=True,
        style={
            "color": "RebeccaPurple",
            "border": "none"
        },
    )
    
    card_vic_total = dbc.Card(
        [
            dbc.CardHeader("Total Victims"),
            dbc.CardBody(
                html.H1(new_df['Count'].sum(), className="card-title"),
            ),
        ],
        className="text-center mb-15",
        style={
            "color": "RebeccaPurple",
            "backgroundColor": "Plum",
        }
    )
    
    card_victim_male = dbc.Card(
        [
            dbc.CardBody(
                html.H2(new_df[new_df.victim_sex_rand == 'Male'].Count.sum(), className="card-title"),
            ),
            dbc.CardImg(src="/assets/images/male.gif", bottom=True, alt="Male gif", style={"width": "100%", "height": "100%", "object-fit": "cover", "border-radius": "20px"}, className="card border-end-0 border-top-0 border-bottom-0 border-5 shadow-lg",),
        ],
        className="text-center mb-2",
        color="light",
        outline=True,
        style={
            "color": "RebeccaPurple",
            "border": "none"
        },
    )
    
    fig7 = go.Figure()
    age_ranges = ["<18", "18-24", "25-44", "45-64", "65+"]
    colors = ['Orchid', 'Violet', 'MediumOrchid', 'DarkOrchid', 'Thistle']

    for age_range, color in zip(age_ranges, colors):
        fig7.add_trace(go.Bar(
            x=['Female', 'Male'],
            y=new_df.loc[new_df['victim_age_rand'] == age_range, "Count"].to_list(),
            name=f'Age {age_range}',
            marker_color=color
        ))

    fig7.update_layout(
        xaxis=dict(
            showgrid=False,
        ),
        yaxis=dict(
            showgrid=False,
        ),
        legend=dict(
            x=0.7,
            y=1.0,
            traceorder='normal',
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15,
        bargroupgap=0.1,
        paper_bgcolor='Lavender',
        plot_bgcolor='Lavender',
        autosize=True,
        margin=dict(t=0, b=0, l=0, r=0),
        height=374,
        title_x=0.5,
        font=dict(
            family="Courier New, monospace",
            size=12,
        ),
    )
    
    return card_victim_female, card_vic_total, card_victim_male, fig7