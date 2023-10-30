# import numpy as np
import pandas as pd
# from sklearn.linear_model import LinearRegression

# import sidebar_menu from the main app.py
from app import sidebar_menu

# app_layout package
import app_layout.main_pane as main_pane

import dash
from dash import html
# from dash.dependencies import Input, Output, State

import plotly.express as px
import plotly.graph_objects as go

### Import Data, better to import from pickle files, rather than importing the script directly
bnb_90d = pd.read_pickle('pickles/october_2023/bnb_90d.pkl')
bnb_gas_fee = pd.read_pickle('pickles/october_2023/bnb_gas_fee.pkl')
bnb_combined_data_final = pd.read_pickle('pickles/october_2023/bnb_combined_data_final.pkl')
bnb_tvl = pd.read_pickle('pickles/october_2023/bnb_tvl.pkl')
bnb_defi_tvl_top10 = pd.read_pickle('pickles/october_2023/bnb_defi_tvl_top10.pkl')


### Section 1: Define the Plots Using Plotly
## fig1: BNB's Price vs. Bitcoin
min_date = min(bnb_90d['Date'])
max_date = max(bnb_90d['Date'])

fig1_data_filtered = bnb_90d[(bnb_90d['Date'] >= max_date - \
                                    pd.Timedelta(days=90)) & (bnb_90d['Date'] \
                                                              <= max_date)]

fig1_trace1 = go.Scatter(x=fig1_data_filtered['Date'], y=fig1_data_filtered\
                                 ['bnb_vs_usd_normalized'], mode='lines', name='BNB vs. USD', \
                                     line={'color': 'green'})

fig1_trace2 = go.Scatter(x=fig1_data_filtered['Date'], y=fig1_data_filtered\
                                 ['bnb_vs_btc_normalized'], mode='lines', name='BNB vs. BTC', \
                                     line={'color': 'gold'})


fig1_layout = go.Layout(
    height=400,
    title='BNB/USD and BNB/BTC - Normalized',
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

fig1 = {"data": [fig1_trace1, fig1_trace2], "layout": fig1_layout}

## fig2: BNB Gas Fee
fig2 = px.bar(bnb_gas_fee, x="Date", y="gasPrice_close", \
              title="BSC Gas Fees (GWEI)", \
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
        html.H1("BNB October 2023 Report", className="title_text", id="title_text_1"),
        html.H5(f"by: Ruddy Setiadi Gunawan", className="note_text", id="note_text_1")
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

## fig3: BNB TVL historical data
min_date_tvl = min(bnb_tvl['Date'])
max_date_tvl = max(bnb_tvl['Date'])

#filter the date range (past 3 years)
fig3_data_filtered = bnb_tvl[(bnb_tvl['Date'] >= max_date_tvl - \
                                    pd.Timedelta(days=1095)) & (bnb_tvl['Date'] \
                                                              <= max_date_tvl)]

fig3_trace = go.Scatter(
    x=fig3_data_filtered['Date'],
    y=fig3_data_filtered['tvl'],
    mode='lines',
    name='bnb_tvl',
    line={'color': 'green'},
    fill='tozeroy',
    fillcolor='rgba(0, 128, 0, 0.2)'
)

fig3_layout = go.Layout(
    height=400,
    title='BNB Historical TVL Past 3 Years',
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

fig3 = {"data": [fig3_trace], "layout": fig3_layout}


## fig4: BNB Top 10 DeFi TVL historical data
bnb_defi_protocol_list_names = ["pancakeswap", "venus", "coinwind", "pinksale", "radiant-v2", \
                                "biswap", "alpaca-finance", "uncx-network", "tranchess-yield", \
                                "helio-protocol"]

colors = ['green', 'red', 'gold', 'blue', 'purple', 'orange', 'pink', 'cyan', 'magenta', 'white']

min_date_tvl_top10 = min(bnb_defi_tvl_top10['Date'])
max_date_tvl_top10 = max(bnb_defi_tvl_top10['Date'])

#filter the date range (past 3 years)
fig4_data_filtered = bnb_defi_tvl_top10[(bnb_defi_tvl_top10['Date'] >= max_date_tvl_top10 - \
                                         pd.Timedelta(days=1095)) & \
                                        (bnb_defi_tvl_top10['Date'] <= max_date_tvl_top10)]

# Generate the traces with the protocol names above
fig4_traces = []
for idx, defi_name in enumerate(bnb_defi_protocol_list_names):
    col_name = f'totalLiquidity_{defi_name}'
    trace = go.Scatter(
        x=fig4_data_filtered['Date'],
        y=fig4_data_filtered[col_name],
        mode='lines',
        name=defi_name.upper(),
        line={'color': colors[idx]}
    )
    fig4_traces.append(trace)

fig4_layout = go.Layout(
    height=400,
    title='Binance (BSC) Top 10 DeFi - TVL Comparison (Past 3 Years)',
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

fig4 = {"data": fig4_traces, "layout": fig4_layout}

# Inform Dash that this is a page
dash.register_page(__name__, title='BNB October 2023 Report')

# Modify the default index string's title
index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>BNB October 2023 Report</title>
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
    sidebar_menu(bnb_combined_data_final),
    main_pane.generate(
        header(),
        key_insights(),
        (fig1, "BNB Price Action vs. USD and BTC", "Description for fig1..."),
        (fig2, "BNB Gas Fees in GWEI", "Description for fig2..."),
        (fig3, "BSC TVL Historical Data (Past 3 Years)", "Description for fig1..."),
        (fig4, "Binance (BSC) Top 10 DeFi - TVL Comparison (Past 3 Years)", "Description for fig2...")
    )
], id='main-container')
