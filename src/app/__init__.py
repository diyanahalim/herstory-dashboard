# app/__init__.py
from dash import Dash
import dash_bootstrap_components as dbc

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY], suppress_callback_exceptions=True)

# Import layout after app initialization to avoid circular imports
from app.layout import layout
app.layout = layout