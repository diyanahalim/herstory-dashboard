
import dash
import dash_bootstrap_components as dbc
from index import server

external_stylesheets = [dbc.themes.MINTY]


# Step 1. Launch the application
app_dash = dash.Dash(__name__, external_stylesheets = external_stylesheets, suppress_callback_exceptions=True)
# Optional: If you need to re-use the server, assign it to app_dash
app_dash.server = server

