"""
Dash Page - ETH October 2023 Report
"""

### Import Libraries
# import sidebar_menu from the main app.py
from app import sidebar_menu

# app_layout package
import app_layout.main_pane as main_pane

import dash
from dash import html

import pandas as pd

import plotly.express as px
import plotly.graph_objects as go


### Import Data, better to import from pickle files, rather than importing the script directly
eth_90d = pd.read_pickle('pickles/october_2023/eth_90d.pkl')
eth_gas_fee = pd.read_pickle('pickles/october_2023/eth_gas_fee.pkl')
eth_combined_data_final = pd.read_pickle('pickles/october_2023/eth_combined_data_final.pkl')
eth_tvl = pd.read_pickle('pickles/october_2023/eth_tvl.pkl')
eth_defi_tvl_top10 = pd.read_pickle('pickles/october_2023/eth_defi_tvl_top10.pkl')


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
    plot_bgcolor='#2b2b2b',
    paper_bgcolor='#2b2b2b',
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
    plot_bgcolor='#2b2b2b',
    paper_bgcolor='#2b2b2b',
    legend={'font': {'color': 'white'}},
    title_font={'color': 'white'}
)

def header():
    return html.Div([
        html.H1("Ethereum (ETH) October 2023 Report", className="title-text", id="title_text_1"),
        html.H5(f"by: Ruddy Setiadi Gunawan", className="note-text", id="note_text_1")
    ])

def key_insights():
    return html.Div([
        html.H3("Key Insights:", className="heading-text", id="key_insight_heading"),
        html.Ul([
            html.Li("ETH has been following the uptrend of BTC against USD in October, but it has been \
                    underperforming against BTC"),
            html.Li("ETH gas fees have been volatile, with a sharp increase observed around October 31st"),
            html.Li("Ethereum historical TVL data has been on a downtrend since its peak in November 2021. \
                    In the recent months, the TVL appeared to stabilize"),
            html.Li("Among top 10 DeFi protocols, Lido still dominates the TVL comparison, followed by Aave \
                    and MakerDAO")
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
    plot_bgcolor='#2b2b2b',
    paper_bgcolor='#2b2b2b',
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
    plot_bgcolor='#2b2b2b',
    paper_bgcolor='#2b2b2b',
    legend={'font': {'color': 'white'}}
)

fig4 = {"data": fig4_traces, "layout": fig4_layout}

# Inform Dash that this is a page
dash.register_page(__name__, title='ETH October 2023 Report')

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
    sidebar_menu(eth_combined_data_final, 'ETH Data - End of Oct 2023'),
    main_pane.generate(
        header(),
        key_insights(),
        (fig1, "ETH Price Action vs. USD and BTC", "The chart above normalizes the starting prices of the two pairs \
            (ETH/USD and ETH/BTC) to assess their relative price actions over the past couple of months. \
            From the visualization, we can infer that from mid-August to late September, Ethereum (ETH) slightly \
            underperformed against USD. Things started to change in the month of October, where ETH has been \
            doing well, following BTC's sharp uptrend against USD. Compared to BTC, however, ETH has been underperforming."),

        (fig2, "Ethereum Gas Fees in GWEI", "Shifting our focus to Ethereum's network data sourced from Owlracle, we \
            explore the average gas fee trends in the month of October. The bar chart paints a picture of the average gas \
            fee progression. There's a clear display of volatility in the gas fees throughout the observed duration. \
            Specifically, around October 31st, the average gas price surged, reaching as high as 19 GWEI. This \
            representation gives us insights into Ethereum's transactional cost fluctuations over this short yet \
            insightful span."),

        (fig3, "Ethereum TVL Historical Data (Past 3 Years)", "Diving into Ethereum's on-chain metrics from DefiLlama \
            over the past three years, the line chart elucidates the trajectory of Ethereum's Total Value Locked (TVL). \
            Starting from November 2020, there was a pronounced climb in TVL, indicating increased activity and trust in \
            the Ethereum ecosystem. By November 2021, Ethereum's TVL reached its peak. This robust growth, however, \
            began to taper post its peak, with a considerable pullback observed as we transitioned into 2023. In the recent \
            months, the TVL appeared to stabilize, showcasing a period of consolidation in the network's value."),

        (fig4, "Ethereum Top 10 DeFi - Historical TVL Comparison", "The last chart shows the TVL comparison among the top \
            DeFi protocols in the Ethereum chain. It is obvious that these projects exhibit distinct trajectories, \
            reflecting their individual dynamisms and market sentiments. Lido still dominates the TVL comparison, \
            followed by Aave and MakerDAO. The rest of the protocols are trailing behind. Interestingly, Lido TVL has \
            been steadily increasing, while Aave and MakerDAO's TVL have been on a downtrend.")
    )
], id='main-container')
