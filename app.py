# import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# from app_layout import sidebar, main_pane
import app_layout.main_pane as main_pane
import app_layout.sidebar as sidebar

import dash
from dash import dcc, html
from dash import dash_table
from dash.dependencies import Input, Output, State

import plotly.express as px
import plotly.graph_objects as go

import dash
from dash import Dash, html, dcc

app = Dash(__name__, use_pages=True)

app.layout = html.Div([
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']}", href=page["relative_path"], style={'color': 'lightblue'}),
            style={
                'backgroundColor': '#2b2b2b',
                'color': 'white',
                'border': '1px solid #ccc',
                'padding': '10px',
                'margin': '10px 0',
                'width': '90%',
                'textAlign': 'left'
            }
        ) for page in dash.page_registry.values()
    ], id='link-container', style={
        'overflowX': 'scroRll',
        'border': '1px solid #ccc',
        'width': '90%',
        'margin': 'auto',
        'backgroundColor': '#3d3d3d'
    }),
    dash.page_container
])


if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=False)


### NOT YET:

# 1. scatter plot between BTC and Gold not yet done in btc_september_2023.py
# 2. eth_october_2023.py has not been completed
# 3. I can already connect different pages in Dash, but they are still outside of sidebar as of now
# 4. customize the homepage