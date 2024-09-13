from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from app import app_dash

# Card Definitions
card_1 = dbc.Card(
    [
        dbc.CardImg(src="/assets/images/Post.png", top=True),
        dbc.CardBody(
            [
                dbc.Button(
                    html.H4("Post It!"),
                    id="collapse-button-1",
                    className="me-1",
                    color="primary",
                    n_clicks=0,
                ),
                dbc.Collapse(
                    dbc.Card(dbc.CardBody(html.P(
                        "Use social media platforms such as Twitter to amplify your voice "
                        "and spread awareness on the incidents to alert others near the location of harassment.",
                        className="card-text",
                    ))),
                    id="collapse-1",
                    is_open=False,
                ),
            ]
        ),
    ],
    style={"width": "18rem"},
)

card_2 = dbc.Card(
    [
        dbc.CardImg(src="/assets/images/Defense.png", top=True),
        dbc.CardBody(
            [
                dbc.Button(
                    html.H4("Woman Up!"),
                    id="collapse-button-2",
                    className="me-1",
                    color="primary",
                    n_clicks=0,
                ),
                dbc.Collapse(
                    dbc.Card(dbc.CardBody(html.P(
                        "Always prepare yourself for the worst, acquire yourself some self-defense moves "
                        "and use them when needed.",
                        className="card-text",
                    ))),
                    id="collapse-2",
                    is_open=False,
                ),
            ]
        ),
    ],
    style={"width": "18rem"},
)

card_3 = dbc.Card(
    [
        dbc.CardImg(src="/assets/images/Talk.png", top=True),
        dbc.CardBody(
            [
                dbc.Button(
                    html.H4("Talk to Your Peers"),
                    id="collapse-button-3",
                    className="me-1",
                    color="primary",
                    n_clicks=0,
                ),
                dbc.Collapse(
                    dbc.Card(dbc.CardBody(html.P(
                        "Let them know about your sexual harassment encounters. "
                        "This could reduce victim blaming when people realize this happens to most of us.",
                        className="card-text",
                    ))),
                    id="collapse-3",
                    is_open=False,
                ),
            ]
        ),
    ],
    style={"width": "18rem"},
)

card_4 = dbc.Card(
    [
        dbc.CardImg(src="/assets/images/Kit.png", top=True),
        dbc.CardBody(
            [
                dbc.Button(
                    html.H4("Protect Yourself"),
                    id="collapse-button-4",
                    className="me-1",
                    color="primary",
                    n_clicks=0,
                ),
                dbc.Collapse(
                    dbc.Card(dbc.CardBody(html.P(
                        "If you feel your body is not strong enough, get yourself a self-defense kit. "
                        "Pepper spray, key knife, taser or even a loud alarm could save you!",
                        className="card-text",
                    ))),
                    id="collapse-4",
                    is_open=False,
                ),
            ]
        ),
    ],
    style={"width": "18rem"},
)

card_5 = dbc.Card(
    [
        dbc.CardImg(src="/assets/images/Alert.png", top=True),
        dbc.CardBody(
            [
                dbc.Button(
                    html.H4("Be Alert"),
                    id="collapse-button-5",
                    className="me-1",
                    color="primary",
                    n_clicks=0,
                ),
                dbc.Collapse(
                    dbc.Card(dbc.CardBody(html.P(
                        "It is fun to walk alone but remember to always be aware of your surroundings. "
                        "Avoid playing with your phone and keep your head up. Don't forget, walk with confidence!",
                        className="card-text",
                    ))),
                    id="collapse-5",
                    is_open=False,
                ),
            ]
        ),
    ],
    style={"width": "18rem"},
)

card_6 = dbc.Card(
    [
        dbc.CardImg(src="/assets/images/Police.png", top=True),
        dbc.CardBody(
            [
                dbc.Button(
                    html.H4("File A Report"),
                    id="collapse-button-6",
                    className="me-1",
                    color="primary",
                    n_clicks=0,
                ),
                dbc.Collapse(
                    dbc.Card(dbc.CardBody(html.P(
                        "If you have been molested or attacked, remember to instantly go to your nearest police station "
                        "to file a report. Know your rights!",
                        className="card-text",
                    ))),
                    id="collapse-6",
                    is_open=False,
                ),
            ]
        ),
    ],
    style={"width": "18rem"},
)

# Layout
layout = html.Div([
    # First row with three cards
    dbc.Row([
        dbc.Col(card_1, width="auto"),
        dbc.Col(card_2, width="auto"),
        dbc.Col(card_3, width="auto"),
    ], justify="center", style={"margin-bottom": "20px"}),
    
    # Second row with three cards
    dbc.Row([
        dbc.Col(card_4, width="auto"),
        dbc.Col(card_5, width="auto"),
        dbc.Col(card_6, width="auto"),
    ], justify="center")
], style={
        "display": "flex", 
        "flex-direction": "column",
        "justify-content": "center",  # Horizontally center
        "align-items": "center",  # Vertically center
        "min-height": "100vh"  # Full viewport height for vertical centering
    })

# Optimized Callback for all collapses
@app_dash.callback(
    Output("collapse-1", "is_open"),
    [Input("collapse-button-1", "n_clicks")],
    [State("collapse-1", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app_dash.callback(
    Output("collapse-2", "is_open"),
    [Input("collapse-button-2", "n_clicks")],
    [State("collapse-2", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app_dash.callback(
    Output("collapse-3", "is_open"),
    [Input("collapse-button-3", "n_clicks")],
    [State("collapse-3", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app_dash.callback(
    Output("collapse-4", "is_open"),
    [Input("collapse-button-4", "n_clicks")],
    [State("collapse-4", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app_dash.callback(
    Output("collapse-5", "is_open"),
    [Input("collapse-button-5", "n_clicks")],
    [State("collapse-5", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app_dash.callback(
    Output("collapse-6", "is_open"),
    [Input("collapse-button-6", "n_clicks")],
    [State("collapse-6", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
