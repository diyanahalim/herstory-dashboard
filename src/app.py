import dash
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.MINTY]

# Step 1. Launch the application
app_dash = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

# Expose the app server as 'server' for Render deployment validation
server = app_dash.server  # Render requires this line for deployment checks