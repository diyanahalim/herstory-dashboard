
import dash
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.MINTY]


# Step 1. Launch the application
app = dash.Dash(__name__, external_stylesheets = external_stylesheets, suppress_callback_exceptions=True)
# Optional: If you need to re-use the server, assign it to app_dash
# server = app_dash.server
server = app.server

# Expose app_dash as app for Render's validation
# app = app_dash