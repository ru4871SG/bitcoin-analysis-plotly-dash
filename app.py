# import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# app_layout package
import app_layout.sidebar as sidebar

import dash
from dash import Dash, dcc, html


def sidebar_menu(data_table):
    return html.Div([
        html.H3('Explore'),
        # Links
        html.Div([
            # Internal Pages
            html.Div(
                dcc.Link(f"{page['name'].title()}", href=page["relative_path"], style={'color': 'lightblue'}),
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
        ] + [
            # External Links to External Websites (Example)
            html.Div([
                html.A("Coingecko", href="https://www.coingecko.com", target="_blank", style={'color': 'lightblue'}),
            ], style={
                'backgroundColor': '#2b2b2b',
                'color': 'white',
                'border': '1px solid #ccc',
                'padding': '10px',
                'margin': '10px 0',
                'width': '90%',
                'textAlign': 'left'
            })
        ], style={
            'overflowX': 'scroll',
            'border': '1px solid #ccc',
            'width': '90%',
            'margin': 'auto',
            'backgroundColor': '#3d3d3d'
        }),

        # Data Table
        html.H3('Data Table'),
        sidebar.generate(data_table)
    ], id='sidebar')


# Use Multiple Pages
app = Dash(__name__, use_pages=True)

app.layout = html.Div([
    dash.page_container
])

# Run the App
if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=False)


### NOT YET:
# 3. customize the homepage and sidebar