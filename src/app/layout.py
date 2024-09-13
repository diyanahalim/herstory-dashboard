# app/layout.py
from dash import html, dcc
import dash_bootstrap_components as dbc
from app.pages import app1, app2, app3, app4, app5, app6

# Define the layout for the Dash app
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [   
        html.H2("HerStory", className="display-4"),
        html.Hr(),
        html.P("Your Voices Are Heard", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink("Overview", active="exact", href="/HerStory/Overview", id="apps/app1-link"),
                dbc.NavLink("Victims' Demographic", active="exact", href="/HerStory/Victims_Demographic", id="apps/app2-link"),
                dbc.NavLink("Suspects' Demographic", active="exact", href="/HerStory/Suspects_Demographic", id="apps/app3-link"),
                dbc.NavLink("Time Variation", active="exact", href="/HerStory/Time_Variation", id="apps/app4-link"),
                dbc.NavLink("Location Variation", active="exact", href="/HerStory/Location_Variation", id="apps/app5-link"),
                dbc.NavLink("Safety Tips", active="exact", href="/HerStory/Safety_Tips", id="apps/app6-link"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

layout = html.Div([dcc.Location(id="url"), sidebar, content])

# Import callback functions to avoid circular import issues
from app import app_dash
from dash.dependencies import Input, Output

@app_dash.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/HerStory/Overview"]:
        return app1.layout
    elif pathname == "/HerStory/Victims_Demographic":
        return app2.layout
    elif pathname == "/HerStory/Suspects_Demographic":
        return app3.layout
    elif pathname == "/HerStory/Time_Variation":
        return app4.layout
    elif pathname == "/HerStory/Location_Variation":
        return app5.layout
    elif pathname == "/HerStory/Safety_Tips":
        return app6.layout
    # Return a 404 message for unrecognized paths
    return dbc.Container(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognized..."),
        ]
    )