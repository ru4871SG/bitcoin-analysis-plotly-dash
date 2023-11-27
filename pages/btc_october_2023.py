"""
Dash Page - BTC October 2023 Report
"""

### Import Libraries
# import sidebar_menu from the main app.py
from app import sidebar_menu

# app_layout package
import app_layout.data_table as data_table
import app_layout.main_pane as main_pane

import dash
from dash import html

import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

from sklearn.linear_model import LinearRegression

### Import Data, better to import from pickle files, rather than importing the script directly
btc_90d_w_external = pd.read_pickle('pickles/october_2023/btc_90d_w_external.pkl')
mempool_stats_30d_grouped = pd.read_pickle('pickles/october_2023/mempool_stats_30d_grouped.pkl')
btc_mining_pools = pd.read_pickle('pickles/october_2023/btc_mining_pools.pkl')
btc_combined_data_final = pd.read_pickle('pickles/october_2023/btc_combined_data_final.pkl')
spot_exchanges_volume = pd.read_pickle('pickles/october_2023/spot_exchanges_volume.pkl')
lightning_mempool_total_capacity = pd.read_pickle('pickles/october_2023/lightning_mempool_total_capacity.pkl')


### Section 1: Define the Plots Using Plotly
## fig1: Bitcoin's Line Chart, with NDX and Gold (Normalized)
min_date = min(btc_90d_w_external['Date'])
max_date = max(btc_90d_w_external['Date'])

fig1_data_filtered = btc_90d_w_external[(btc_90d_w_external['Date'] >= max_date - \
                                    pd.Timedelta(days=90)) & (btc_90d_w_external['Date'] \
                                                              <= max_date)]

fig1_trace1 = go.Scatter(x=fig1_data_filtered['Date'], y=fig1_data_filtered\
                                 ['btc_price_normalized'], mode='lines', name='BTC', \
                                     line={'color': 'green'})

fig1_trace2 = go.Scatter(x=fig1_data_filtered['Date'], y=fig1_data_filtered\
                                 ['ndx_price_normalized'], mode='lines', name='NASDAQ 100', \
                                     line={'color': 'red'})

fig1_trace3 = go.Scatter(x=fig1_data_filtered['Date'], y=fig1_data_filtered\
                                 ['gold_price_normalized'], mode='lines', name='Gold', \
                                     line={'color': 'gold'})


fig1_layout = go.Layout(
    height=400,
    title='BTC vs. NDX vs. Gold - Normalized',
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

fig1 = {"data": [fig1_trace1, fig1_trace2, fig1_trace3], "layout": fig1_layout}

## fig2: Scatter Plot Between BTC vs. NDX (Normalized)
# Extract the month name from the 'Date' column and store it in a new 'Month' column
btc_90d_w_external_and_months = btc_90d_w_external.copy()
btc_90d_w_external_and_months['Month'] = btc_90d_w_external_and_months['Date'].dt.strftime('%B')

# Compute linear regression line using sklearn (BTC vs. NDX)
X = btc_90d_w_external_and_months["btc_price_normalized"].values.reshape(-1, 1)
y = btc_90d_w_external_and_months["ndx_price_normalized"].values
model = LinearRegression().fit(X, y)
y_pred = model.predict(X)

# define fig2 - BTC vs. NDX
fig2 = px.scatter(btc_90d_w_external_and_months, x='btc_price_normalized',
                  y='ndx_price_normalized',
                  color='Month',
                  labels={'btc_price_normalized': 'BTC',
                  'ndx_price_normalized': 'NDX'}, 
                  title='BTC vs. NDX')

# Add linear regression line to fig2
fig2.add_trace(go.Scatter(x=btc_90d_w_external_and_months["btc_price_normalized"], \
                          y=y_pred, mode='lines', name='Trend Line', line={'color': '#dfbd75'}))

fig2_layout = fig2.layout

fig2_layout.update(
    height=400,
    plot_bgcolor='#2b2b2b',
    paper_bgcolor='#2b2b2b',
    yaxis={
        'gridcolor': '#636363',
        'zerolinecolor': '#636363',
        'tickfont': {'color': 'white'},
        'titlefont': {'color': 'white'}
    },
    xaxis={
        'gridcolor': '#636363',
        'zerolinecolor': '#636363',
        'tickfont': {'color': 'white'},
        'titlefont': {'color': 'white'}
    },
    legend={'font': {'color': 'white'}},
    title_font={'color': 'white'}
)

fig2 = {"data": fig2.data, "layout": fig2_layout}

## fig2b: Scatter Plot Between BTC vs. Gold (Normalized)
# Compute linear regression line for fig2b using sklearn (BTC vs. Gold)
X_2b = btc_90d_w_external_and_months["btc_price_normalized"].values.reshape(-1, 1)
y_2b = btc_90d_w_external_and_months["gold_price_normalized"].values
model_2b = LinearRegression().fit(X_2b, y_2b)
y_2b_pred = model_2b.predict(X_2b)

# define fig2b - BTC vs Gold
fig2b = px.scatter(btc_90d_w_external_and_months, x='btc_price_normalized',
                  y='gold_price_normalized',
                  color='Month',
                  labels={'btc_price_normalized': 'BTC',
                  'gold_price_normalized': 'GOLD'}, 
                  title='BTC vs. GOLD')

# Add linear regression line to fig2b
fig2b.add_trace(go.Scatter(x=btc_90d_w_external_and_months["btc_price_normalized"], \
                          y=y_2b_pred, mode='lines', name='Trend Line', line={'color': '#dfbd75'}))

fig2b_layout = fig2b.layout

fig2b_layout.update(
    height=400,
    plot_bgcolor='#2b2b2b',
    paper_bgcolor='#2b2b2b',
    yaxis={
        'gridcolor': '#636363',
        'zerolinecolor': '#636363',
        'tickfont': {'color': 'white'},
        'titlefont': {'color': 'white'}
    },
    xaxis={
        'gridcolor': '#636363',
        'zerolinecolor': '#636363',
        'tickfont': {'color': 'white'},
        'titlefont': {'color': 'white'}
    },
    legend={'font': {'color': 'white'}},
    title_font={'color': 'white'}
)

fig2b = {"data": fig2b.data, "layout": fig2b_layout}

## fig3: Bitcoin Median Tx Fee Over Time
fig3 = px.bar(mempool_stats_30d_grouped, x="block_group", y="medianFee", \
              title="Bitcoin Median Tx Fee Over Time", \
              color_discrete_sequence=['#a2823c'], \
              hover_data={"block_group": False, "medianFee": False}, \
              custom_data=['block_group', 'medianFee', 'height'])

fig3.update_traces(hovertemplate="<b>Block Height Group:</b> %{customdata[0]}<br>\
              <b>Median Fee:</b> %{customdata[1]:.0f} sat/vB<br><b>End of Block Height:</b> %{customdata[2]:.0f}")

# Set the x-axis label, y-axis label and adjust the x-axis tick angle
fig3.update_layout(
    yaxis={
        'gridcolor': '#636363',
        'zerolinecolor': '#636363',
        'tickfont': {'color': 'white'},
        'titlefont': {'color': 'white'}
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


## fig4: Bitcoin Mining Pools
# Get the top 10 mining pools by block count
top_10_pools = btc_mining_pools.sort_values(by='blockCount', ascending=False).head(10)

# Group the outside top 10 mining pools as "Others"
other_pools = btc_mining_pools[~btc_mining_pools['name'].isin(top_10_pools['name'])]
other_block_count = other_pools['blockCount'].sum()
other_pools = pd.DataFrame({'name': ['Others'], 'blockCount': [other_block_count]})

# Concatenate the top 10 mining pools and the "Others" group
pools = pd.concat([top_10_pools, other_pools])

# Calculate the percentage of block count for each pool
pools['percentage'] = pools['blockCount'] / pools['blockCount'].sum() * 100

fig4 = px.pie(pools, values='blockCount', names='name', title='Bitcoin Mining Pools',\
              hover_data=['percentage'])

# Show the percentage and edit the location of the percentage numbers
fig4.update_traces(
    hovertemplate='<b>%{label}</b><br>' +
                  'blockCount: %{value}<br>' +
                  'Percentage: %{customdata[0]:.2f}%<extra></extra>',
    textposition='outside',
    textinfo='percent+label',
    insidetextorientation='radial',
    textfont={'color': 'white'}
)

# Set the x-axis label, y-axis label and adjust the x-axis tick angle
fig4.update_layout(
    yaxis={
        'gridcolor': '#636363',
        'zerolinecolor': '#636363',
        'tickfont': {'color': 'white'},
        'titlefont': {'color': 'white'}
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


## fig5: Exchange Data (Spot)
# Create the traces for each exchange
exchange_names = ["binance", "gdax", "kraken", "kucoin", "bitstamp", 
                  "okex", "bitfinex", "huobi", "gemini"]

# Custom display names for the legend
display_names = {
    "binance": "Binance",
    "gdax": "Coinbase",
    "kraken": "Kraken",
    "kucoin": "Kucoin",
    "bitstamp": "Bitstamp",
    "okex": "OKX",
    "bitfinex": "Bitfinex",
    "huobi": "Huobi",
    "gemini": "Gemini"
}

traces = []

for exchange in exchange_names:
    vol_column = f"{exchange}_vol_in_btc"
    trace = go.Scatter(
        x=spot_exchanges_volume['date'], 
        y=spot_exchanges_volume[vol_column],
        mode='lines', 
        name=display_names[exchange],
        text=[
            f"<b>Exchange: {display_names[exchange]}</b><br>Trading Vol.: {vol:,.2f} BTC<br>Date: {date}"
            for vol, date in zip(spot_exchanges_volume[vol_column], spot_exchanges_volume['date'])
        ],
        hoverinfo='text'
    )
    traces.append(trace)

layout_fig5 = go.Layout(
    title='Trading Volumes of Spot Exchanges',
    xaxis={'title': 'Date', 'gridcolor': '#636363', 'zerolinecolor': '#636363', \
           'tickfont': {'color': 'white'}, 'titlefont': {'color': 'white'}},
    yaxis={'title': 'Volume in BTC', 'gridcolor': '#636363', 'zerolinecolor': '#636363', \
           'tickfont': {'color': 'white'}, 'titlefont': {'color': 'white'}},
    plot_bgcolor='#2b2b2b',
    paper_bgcolor='#2b2b2b',
    legend={'font': {'color': 'white'}},
    title_font={'color': 'white'}
)

fig5 = go.Figure(data=traces, layout=layout_fig5)


## fig6: Lightning Network Stats
trace1 = go.Scatter(x=lightning_mempool_total_capacity['added'],
                    y=lightning_mempool_total_capacity['total_capacity'],
                    mode='lines',
                    name='Total Capacity',
                    yaxis='y1',
                    text=['Total Capacity: {:.0f}'.format(val) \
                          for val in lightning_mempool_total_capacity['total_capacity']],
                    hoverinfo='text+y+x',
                    hovertemplate='<b>%{text}</b><br>' + '<b>Date</b>: %{x}<extra></extra>')

trace2 = go.Scatter(x=lightning_mempool_total_capacity['added'],
                    y=lightning_mempool_total_capacity['channel_count'],
                    mode='lines',
                    name='Channel Count',
                    yaxis='y2',
                    text=['Channel Count: {:.0f}'.format(val) \
                          for val in lightning_mempool_total_capacity['channel_count']],
                    hoverinfo='text+y+x',
                    hovertemplate='<b>%{text}</b><br>' + '<b>Date</b>: %{x}<extra></extra>')

layout_fig6 = go.Layout(
    title='Mempool Stats - Lightning Network',
    title_font={'color': 'white'},
    xaxis={
        'title': 'Date',
        'gridcolor': '#636363',
        'zerolinecolor': '#636363',
        'tickfont': {'color': 'white', 'size': 10},
        'titlefont': {'color': 'white'}
    },
    yaxis={
        'title': 'Total Capacity',
        'side': 'left',
        'showgrid': False,
        'gridcolor': '#636363',
        'zerolinecolor': '#636363',
        'tickfont': {'color': 'white', 'size': 8},
        'titlefont': {'color': 'white'}
    },
    yaxis2={
        'title': 'Channel Count',
        'side': 'right',
        'overlaying': 'y',
        'showgrid': False,
        'gridcolor': '#636363',
        'zerolinecolor': '#636363',
        'tickfont': {'color': 'white', 'size': 8},
        'titlefont': {'color': 'white'}
    },
    plot_bgcolor='#2b2b2b',
    paper_bgcolor='#2b2b2b',
    legend={'font': {'color': 'white'}}
)

fig6 = go.Figure(data=[trace1, trace2], layout=layout_fig6)


### Section 2: Define the App Layout and Texts
def header():
    return html.Div([
        html.H1("Bitcoin (BTC) October 2023 Report", className="title-text", id="title_text_1"),
        html.H5(f"by: Ruddy Setiadi Gunawan", className="note-text", id="note_text_1")
    ])

def key_insights():
    return html.Div([
        html.H3("Key Insights:", className="heading-text", id="key_insight_heading"),
        html.Ul([
            html.Li("In October 2023, Bitcoin price action has been doing much better than NDX and Gold"),
            html.Li("Bitcoin has not been positively correlated with NDX, but it's still positively \
                    correlated with Gold"),
            html.Li("Foundry USA and AntPool are still leading the mining pool distribution"),
            html.Li("Binance is still leading the spot trading volume data, with peak activities around \
                    August 18th and October 24th"),
            html.Li("There has been an inverse relationship between total capacity and channel count for \
                    Lightning Network (LN) in the month of October")
        ], className="bullet-points", id="bullet_points_list"),
    ])

# Inform Dash that this is a page
dash.register_page(__name__, title='BTC October 2023 Report')

# Modify the default index string's title
index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Bitcoin October 2023 Report</title>
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
    sidebar_menu(),
    main_pane.generate(
        header(),
        key_insights(),
        (fig1, "Bitcoin Price Action vs. NDX and Gold", "The above chart normalized the starting prices of the three assets \
            (BTC, NDX, and Gold) to check their price actions' correlation over the past 3 months. As depicted in the chart, \
            from mid-August to late September, Bitcoin underperformed compared to Nasdaq-100 (NDX) and Gold. However, \
            starting October, Bitcoin exhibited a sharp uptrend, significantly outpacing both NDX and Gold. The sharp uptrend \
            was primarily driven by speculation and optimism over the potential approval of a Bitcoin spot exchange-traded \
            fund (ETF) in the United States. Anyway, BTC/Gold seems to be more correlated as compared to BTC/NDX."),

        (fig2, "Correlation Analysis: Bitcoin vs. NDX", "My second analysis utilizes EDA (Exploratory Data Analysis) with a \
            scatter plot to evaluate the correlation between Bitcoin and NDX. From the scatter plot, one can observe a \
            descending trend, suggesting an inverse correlation between Bitcoin and NDX over the given period. The linear \
            regression line further emphasizes this inverse relationship. Notably, data points from October are more \
            dispersed from the trend line than those from August and September, indicating greater variability during \
            that month. This suggests that the price action of Bitcoin in October deviated more significantly from the \
            trend of NDX."),

        (fig2b, "Correlation Analysis: Bitcoin vs. Gold", "The third analysis is using a scatter plot, just like the \
            previous analysis but it uses gold price as the y-axis while the x-axis remains BTC. This scatter plot \
            highlights a rising trend, pointing to a direct correlation between the two over the analyzed period. \
            The linear regression line further corroborates this positive relationship. Noteworthy is the distribution \
            of data points; those from August and September cluster more closely to the trend line, while October's \
            points are more scattered, indicating a heightened variability in that month."),

        (fig3, "Bitcoin Block Analysis - Median Tx Fee", "Turning our attention to the Bitcoin block data sourced directly \
            from the mempool, we delve into the median transaction (tx) fee trends over the past 30 blocks, which can be \
            approximated as a month if considering 144 blocks per day. The bar chart provides insights into the median tx fee \
            trajectory. It's evident that there's been noticeable variability in the median tx fees over the considered \
            timeframe. For block height group 23, the median transaction fee spiked, with 27 sat/vB. However, post this \
            surge, there's been a decline in fees. To facilitate a more streamlined analysis, the data is presented in \
            block groups, each representing 144 blocks. This grouping is based on Bitcoin's average mining rate of 144 \
            blocks daily."),

        (fig4, "Bitcoin Mining Pools", "This section analyzes Bitcoin mining pools' distribution from mempool. Just like \
            in the previous month, Foundry USA and AntPool are still leading the distribution, with F2Pool, ViaBTC, \
            and BinancePool following behind them closely. The mining pools' distribution in the Bitcoin network is well \
            diversified, as you can see from the pie chart above. Interestingly, smaller pools like MARA and LUXOR \
            have also carved out their niche in the network. It's essential to monitor these distributions regularly as \
            shifts in mining power can influence the overall security and decentralization of the Bitcoin network"),

        (fig5, "Spot Exchanges Volume Data", "Let's check the cryptocurrency spot exchanges' volume data. \
            The above chart shows that Binance still dominates the market as always, with peak activities around August \
            18th and October 24th. The activities around October 24th makes a lot of sense considering the sharp uptrend \
            of Bitcoin price action around that time. While Binance leads the pack, other exchanges like Coinbase and \
            Kraken maintain consistent trading volumes throughout the period. It's noteworthy that despite the dominance \
            of Binance, the market landscape remains competitive with different exchanges vying for a significant share \
            of the trading volume."),

        (fig6, "Lightning Network (LN) Data", "Now, let's analyze the Lightning Network (LN) data. When it comes to LN, \
            the more capacity the network has, the more value it can transfer at any given time without needing to \
            open new channels. As for channel count, a higher channel count suggests a more interconnected and \
            potentially more decentralized network. Looks like there has been an inverse relationship between the two \
            in the month of October.")
    ),
    data_table.generate(btc_combined_data_final, "Bitcoin Data Table - End of Oct 2023")
], id='main-container')
