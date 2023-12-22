"""
Dash Page - ETH November 2023 Report
"""

### Import Libraries
from app import header

import shared_functions.data_table as data_table
import shared_functions.main_pane as main_pane

import dash
from dash import html

import pandas as pd

import plotly.express as px
import plotly.graph_objects as go


### Import Data, better to import from pickle files, rather than importing the script directly
eth_90d = pd.read_pickle('pickles/november_2023/eth_90d.pkl')
eth_gas_fee = pd.read_pickle('pickles/november_2023/eth_gas_fee.pkl')
eth_combined_data_final = pd.read_pickle('pickles/november_2023/eth_combined_data_final.pkl')
eth_tvl = pd.read_pickle('pickles/november_2023/eth_tvl.pkl')
eth_defi_tvl_top10 = pd.read_pickle('pickles/november_2023/eth_defi_tvl_top10.pkl')


### Section 1: Define the Plots Using Plotly
## fig1: ETH Price vs. USD and Bitcoin
min_date = min(eth_90d['Date'])
max_date = max(eth_90d['Date'])

fig1_data_filtered = eth_90d[(eth_90d['Date'] >= max_date - \
                                    pd.Timedelta(days=90)) & (eth_90d['Date'] \
                                                              <= max_date)]

fig1_trace1 = go.Scatter(x=fig1_data_filtered['Date'], y=fig1_data_filtered\
                                 ['eth_vs_usd_normalized'], mode='lines', name='ETH vs. USD', \
                                     line={'color': 'green'})

fig1_trace2 = go.Scatter(x=fig1_data_filtered['Date'], y=fig1_data_filtered\
                                 ['eth_vs_btc_normalized'], mode='lines', name='ETH vs. BTC', \
                                     line={'color': 'gold'})


fig1_layout = go.Layout(
    height=400,
    title='ETH/USD and ETH/BTC - Normalized',
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
    plot_bgcolor='#171713',
    paper_bgcolor='#171713',
    legend={'font': {'color': 'white'}}
)

fig1 = {"data": [fig1_trace1, fig1_trace2], "layout": fig1_layout}

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
    plot_bgcolor='#171713',
    paper_bgcolor='#171713',
    legend={'font': {'color': 'white'}},
    title_font={'color': 'white'}
)

### Section 2: Define the App Layout and Texts

def key_insights():
    return html.Div([
        html.H1("Ethereum (ETH) November 2023 Report", className="title-text", id="title_text_1"),
        html.H5(f"by: Ruddy Setiadi Gunawan", className="note-text", id="note_text_1"),
        html.H3("Key Insights:", className="heading-text", id="key_insight_heading"),
        html.Ul([
            html.Li("ETH has been going up against USD in both October and November, but it's still \
                    underperforming against BTC."),
            html.Li("ETH gas fees have been volatile, with the peak of 100 GWEI on November 20th."),
            html.Li("Ethereum TVL graph began to trend upward again recently, following ETH's positive \
                    price action."),
            html.Li("Just like the previous month, Lido still dominates the TVL comparison, followed by Aave \
                    and MakerDAO.")
        ], className="bullet-points", id="bullet_points_list"),
    ])

## fig3: Ethereum TVL historical data
min_date_tvl = min(eth_tvl['Date'])
max_date_tvl = max(eth_tvl['Date'])

#filter the date range (past 3 years)
fig3_data_filtered = eth_tvl[(eth_tvl['Date'] >= max_date_tvl - \
                                    pd.Timedelta(days=1095)) & (eth_tvl['Date'] \
                                                              <= max_date_tvl)]

fig3_trace = go.Scatter(
    x=fig3_data_filtered['Date'],
    y=fig3_data_filtered['tvl'],
    mode='lines',
    name='eth_tvl',
    line={'color': 'green'},
    fill='tozeroy',
    fillcolor='rgba(0, 128, 0, 0.2)'
)

fig3_layout = go.Layout(
    height=400,
    title='Ethereum Historical TVL Past 3 Years',
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
    plot_bgcolor='#171713',
    paper_bgcolor='#171713',
    legend={'font': {'color': 'white'}}
)

fig3 = {"data": [fig3_trace], "layout": fig3_layout}


## fig4: Ethereum Top 10 DeFi TVL historical data
eth_defi_protocol_list_names = ["aave", "lido", "makerdao", "uniswap", "summer.fi", "instadapp", \
                                "compound", "rocket-pool", "curve-dex", "convex-finance"]

colors = ['green', 'red', 'gold', 'blue', 'purple', 'orange', 'pink', 'cyan', 'magenta', 'white']

min_date_tvl_top10 = min(eth_defi_tvl_top10['Date'])
max_date_tvl_top10 = max(eth_defi_tvl_top10['Date'])

#filter the date range (past 3 years)
fig4_data_filtered = eth_defi_tvl_top10[(eth_defi_tvl_top10['Date'] >= max_date_tvl_top10 - \
                                         pd.Timedelta(days=1095)) & \
                                        (eth_defi_tvl_top10['Date'] <= max_date_tvl_top10)]

# Generate the traces with the protocol names above
fig4_traces = []
for idx, defi_name in enumerate(eth_defi_protocol_list_names):
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
    title='Ethereum Top 10 DeFi - Historical TVL Comparison',
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
    plot_bgcolor='#171713',
    paper_bgcolor='#171713',
    legend={'font': {'color': 'white'}}
)

fig4 = {"data": fig4_traces, "layout": fig4_layout}

# Inform Dash that this is a page
dash.register_page(__name__, title='ETH November 2023 Report')

# Modify the default index string's title
index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Ethereum November 2023 Report</title>
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
    html.Div([

    main_pane.generate(
        header(),
        key_insights(),
        (fig1, "ETH Price Action vs. USD and BTC", "The chart above normalizes the starting prices of the two pairs \
            (ETH/USD and ETH/BTC) to assess their relative price actions over the past couple of months. \
            From the visualization, we can see that ETH has been doing quite well against USD recently. However \
            they have been underperforming against BTC."),

        (fig2, "Ethereum Gas Fees in GWEI", "Shifting our focus to Ethereum's network data sourced from Owlracle, we \
            explore the average gas fee trends in the month of November. The bar chart paints a picture of the average gas \
            fee progression. There's a clear display of volatility in the gas fees throughout the observed duration. \
            Specifically, around November 20th, the average gas price surged, reaching as high as 100 GWEI."),

        (fig3, "Ethereum TVL Historical Data (Past 3 Years)", "Diving into Ethereum's on-chain metrics from DefiLlama \
            over the past three years, the line chart shows the historical movement of Ethereum's Total Value Locked (TVL). \
            Starting from December 2020, there was a significant climb in TVL, indicating increased activity and trust in \
            the Ethereum ecosystem. By November 2021, Ethereum's TVL reached its peak. This growth, however, \
            didn't last, with a noticeable pullback as we transitioned into 2023. In the past one month, the TVL began \
            to trend upward again, following ETH's positive price action."),

        (fig4, "Ethereum Top 10 DeFi - Historical TVL Comparison", "The last chart shows the TVL comparison among the top \
            DeFi protocols in the Ethereum chain. Many of these projects show different trends over time, \
            reflecting the market appetite has not always been the same for these DeFi projects. Just like the previous \
            month, Lido still dominates the TVL comparison, and it's been trending upward for quite some time. \
            Aave and MakerDAO, on the other hand, used to be in a downward trend, but they have been showing a reversal trend \
            since mid October 2023.")
    ),
    data_table.generate(eth_combined_data_final, "Ethereum Data Table - End of Nov 2023")
    ], className='main'),
    html.Div([
        html.Img(src="assets/icons/ellipse.svg", alt=""),
    ],className="ellipse")
], id='main-container')
