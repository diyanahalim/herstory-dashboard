
import dash
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.MINTY]


# Step 1. Launch the application
app_dash = dash.Dash(__name__, external_stylesheets = external_stylesheets, suppress_callback_exceptions=True)
server = app_dash.server  # Expose the server for deployment

