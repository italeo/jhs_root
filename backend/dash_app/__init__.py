# Initializes the Dash app
from dash import Dash

def create_dash_app(server):
    dash_app = Dash(__name__, server=server, url_base_pathname='/dash/')
    dash_app.title = 'Dash App'
    return dash_app
