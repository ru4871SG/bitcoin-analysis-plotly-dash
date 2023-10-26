# import numpy as np
import pandas as pd
# from sklearn.linear_model import LinearRegression

# import generate_sidebar from the main app.py
from app import generate_sidebar

# app_layout package
import app_layout.main_pane as main_pane

import dash
from dash import html
# from dash.dependencies import Input, Output, State

import plotly.express as px
import plotly.graph_objects as go

### Import Data, better to import from pickle files, rather than importing the script directly
eth_90d = pd.read_pickle('pickles/october_2023/eth_90d.pkl')
eth_gas_fee = pd.read_pickle('pickles/october_2023/eth_gas_fee.pkl')
eth_combined_data_final = pd.read_pickle('pickles/october_2023/eth_combined_data_final.pkl')

### Section 1: Define the Plots Using Plotly
## fig1: Ethereum's Price vs. Bitcoin
min_date = min(eth_90d['Date'])
max_date = max(eth_90d['Date'])

fig1_data_filtered = eth_90d[(eth_90d['Date'] >= max_date - \
                                    pd.Timedelta(days=90)) & (eth_90d['Date'] \
                                                              <= max_date)]

fig1_trace1 = go.Scatter(x=fig1_data_filtered['Date'], y=fig1_data_filtered\
                                 ['price_vs_btc'], mode='lines', name='eth', \
                                     line={'color': 'green'})


fig1_layout = go.Layout(
    height=400,
    title='ETH vs. BTC Price Action',
    titlefont={'color': 'white'},
    title_x=0.05,
    yaxis={
        'gridcolor': '#636363',
        'zerolinecolor': '#636363',
        'tickfont': {'color': 'white'},
        'titlefont': {'color': 'white'},
        'title': ''
    },
    xaxis={
        'gridcolor': '#636363',
        'zerolinecolor': '#636363',
        'tickfont': {'color': 'white'}
    },
    plot_bgcolor='#2b2b2b',
    paper_bgcolor='#2b2b2b',
    legend={'font': {'color': 'white'}}
)

fig1 = {"data": [fig1_trace1], "layout": fig1_layout}

## fig2: Ethereum Gas Fee
fig2 = px.bar(eth_gas_fee, x="Date", y="gasPrice_close", \
              title="ETH Gas Fees (GWEI)", \
              color_discrete_sequence=['#a2823c'], \
              hover_data={"Date": False, "gasPrice_close": False}, \
              custom_data=['Date', 'gasPrice_close'])

fig2.update_traces(hovertemplate="<b>Date:</b> %{customdata[0]}<br><b>Gas Price (Close):</b> %{customdata[1]:.0f} GWEI")

fig2.update_layout(
    yaxis={
        'gridcolor': '#636363',
        'zerolinecolor': '#636363',
        'tickfont': {'color': 'white'},
        'titlefont': {'color': 'white'},
        'title': ''
    },
    xaxis={
        'gridcolor': '#636363',
        'zerolinecolor': '#636363',
        'tickfont': {'color': 'white'},
        'titlefont': {'color': 'white'}
    },
    plot_bgcolor='#2b2b2b',
    paper_bgcolor='#2b2b2b',
    legend={'font': {'color': 'white'}},
    title_font={'color': 'white'}
)

def header():
    return html.Div([
        html.H1("Ethereum (ETH) October 2023 Report", className="title_text", id="title_text_1"),
        html.H5(f"by: Ruddy Setiadi Gunawan", className="author_text", id="author_text_1")
    ])

def key_insights():
    return html.Div([
        html.H3("Key Insights:", className="heading_text", id="key_insight_heading"),
        html.Ul([
            html.Li("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod"),
            html.Li("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod"),
            html.Li("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod"),
            html.Li("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod"),
            html.Li("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod")
        ], className="bullet_points", id="bullet_points_list"),
    ])

# Inform Dash that this is a page
dash.register_page(__name__)

# Modify the default index string's title
index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Ethereum October 2023 Report</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Define the app layout for this page
layout = html.Div([
    generate_sidebar(eth_combined_data_final),
    main_pane.generate(
        header(),
        key_insights(),
        (fig1, "Ethereum vs. BTC Price action", "Description for fig1..."),
        (fig2, "Ethereum Gas Fees in GWEI", "Description for fig2...")
    )
], id='main-container')
