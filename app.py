# import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# app_layout package
import app_layout.sidebar as sidebar

import dash
from dash import Dash, html, dcc

# generate sidebar, including internal pages - mobile layout is not yet done, fix this later, 
# including Mobile and Tablet Layouts in styles.css 
def generate_sidebar(data_table):
    return html.Div([
        # Links
        html.Div([
            # Internal Pages
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
        ] + [
            # External Links to External Websites (Example)
            html.Div([
                html.A("Google", href="https://www.google.com", target="_blank", style={'color': 'lightblue'}),
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
        html.H4('Data Table'),
        sidebar.generate(data_table)
    ], id='sidebar', style={'width': '25%', 'float': 'left'})


# Use Multiple Pages
app = Dash(__name__, use_pages=True)

app.layout = html.Div([
    dash.page_container
])

# Run the App
if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=False)


### NOT YET:

# 1. scatter plot between BTC and Gold not yet done in btc_september_2023.py
# 2. eth_october_2023.py has not been completed
# 3. customize the homepage and sidebar
# 4. sidebar is not working properly for mobile responsiveness, previously it followed the correct instructions in style.css