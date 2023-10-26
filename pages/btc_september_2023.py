# import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

import app_layout.main_pane as main_pane
import app_layout.sidebar as sidebar

import dash
from dash import dcc, html
from dash import dash_table
from dash.dependencies import Input, Output, State

import plotly.express as px
import plotly.graph_objects as go

### Import Data, better to import from pickle files, rather than importing the script directly
btc_90d_w_external = pd.read_pickle('pickles/september_2023/btc_90d_w_external.pkl')
mempool_stats_30d_grouped = pd.read_pickle('pickles/september_2023/mempool_stats_30d_grouped.pkl')
btc_mining_pools = pd.read_pickle('pickles/september_2023/btc_mining_pools.pkl')
btc_combined_data_final = pd.read_pickle('pickles/september_2023/btc_combined_data_final.pkl')
spot_exchanges_volume = pd.read_pickle('pickles/september_2023/spot_exchanges_volume.pkl')
lightning_mempool_total_capacity = pd.read_pickle('pickles/september_2023/lightning_mempool_total_capacity.pkl')

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

## fig2: Scatter Plot Between BTC vs. NDX and BTC vs. Gold (Normalized)
# Extract the month name from the 'Date' column and store it in a new 'Month' column
btc_90d_w_external_and_months = btc_90d_w_external.copy()
btc_90d_w_external_and_months['Month'] = btc_90d_w_external_and_months['Date'].dt.strftime('%B')

# Compute linear regression line using sklearn
X = btc_90d_w_external_and_months["btc_price_normalized"].values.reshape(-1, 1)
y = btc_90d_w_external_and_months["ndx_price_normalized"].values
model = LinearRegression().fit(X, y)
y_pred = model.predict(X)

# define fig2
fig2 = px.scatter(btc_90d_w_external_and_months, x='btc_price_normalized',
                 y='ndx_price_normalized',
                  color='Month',   # Use the 'Month' column for the color
                  labels={'btc_price_normalized': 'BTC',
                      'ndx_price_normalized': 'NDX'}, 
                  title='BTC vs. NDX')

# Add linear regression line (Trend Line) to fig2
fig2.add_trace(go.Scatter(x=btc_90d_w_external_and_months["btc_price_normalized"], \
                          y=y_pred, mode='lines', name='Trend Line', line={'color': 'blue'}))

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

# define the options for the y-axis dropdown not yet

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
    xaxis={'title': 'Date', 'gridcolor': '#636363', 'zerolinecolor': '#636363', 'tickfont': {'color': 'white'}, 'titlefont': {'color': 'white'}},
    yaxis={'title': 'Volume in BTC', 'gridcolor': '#636363', 'zerolinecolor': '#636363', 'tickfont': {'color': 'white'}, 'titlefont': {'color': 'white'}},
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
        html.H1("Bitcoin (BTC) September 2023 Report", className="title_text", id="title_text_1"),
        html.H5(f"by: Ruddy Setiadi Gunawan", className="author_text", id="author_text_1")
    ])

def key_insights():
    return html.Div([
        html.H3("Key Insights:", className="heading_text", id="key_insight_heading"),
        html.Ul([
            html.Li("In Q3 2023, Bitcoin price action has not been tightly correlated to NDX or Gold"),
            html.Li("In the month of September, Bitcoin median tx fee were usually low, peaked at 29 sat/vB"),
            html.Li("Foundry USA and AntPool are still leading the mining pool distribution"),
            html.Li("Binance is still leading the spot trading volume data, with peak activities around July 14th and August 18th"),
            html.Li("Lightning Network stats have been stagnant in the past 3 months")
        ], className="bullet_points", id="bullet_points_list"),
    ])

# Inform Dash that this is a page
dash.register_page(__name__, path='/')

# Modify the default index string's title
index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Bitcoin September 2023 Report</title>
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

layout = html.Div([
    sidebar.generate(btc_combined_data_final),
    main_pane.generate(
        header(),
        key_insights(),
        (fig1, "Bitcoin Price Action vs. NDX and Gold", "The above chart normalized the starting prices of the three objects (BTC, NDX, and \
         Gold) to make it easier to see their correlation. As you can see in the above chart, \
            Bitcoin has been underperforming from early July to end of September compared to NDX and Gold. \
                On August 16th, Bitcoin suffered a heavy bearish pressure, and it never \
                    really recovered ever since. Meanwhile, NDX and Gold have been much more \
                        stable compared to Bitcoin. It remains to be seen whether Bitcoin price action \
                            will eventually follow NDX or Gold again"),

        (fig2, "Correlation Analysis: Bitcoin vs. NDX and Gold", "My second analysis uses EDA (Exploratory data analysis) with scatter plots to \
               check the correlation between Bitcoin vs. NDX and Bitcoin vs. Gold. Both scatter \
               plots show moderate correlation, although they are not tightly correlated. I have \
               also included the linear regression (trend) line so you can check the consistencies \
               of the data points against the trend line."),

        (fig3, "Bitcoin Block Analysis - Median Tx Fee", "Now, let's check the Bitcoin block data directly from mempool to see the median \
               transaction (tx) fee for the past 30 days. I used mempool's data because it is a \
               widely trusted blockchain explorer in the Bitcoin community. Looks like the median \
               tx fees have not fluctuated much in the past 30 days. Around September 19th (end of \
               the block height 808519), the median transaction fee peaked at 29 sat/vB, but it's \
               been trending down ever since, signaling a lack of trading activities in the Bitcoin \
               blockchain. To analyze the median tx fee, I grouped every 144 blocks into just one \
               block group. On average, Bitcoin mines 144 blocks per day."),

        (fig4, "Bitcoin Mining Pools", "This section analyzes Bitcoin mining pools' distribution from mempool. Foundry \
                   USA and AntPool are still leading the distribution, with F2Pool, ViaBTC, \
                   and BinancePool following behind them closely. The mining pools' distribution \
                   in the Bitcoin network is well diversified, as you can see from the pie chart \
                   above, and it's much more decentralized than most altcoins in the \
                   cryptocurrency industry."),

        (fig5, "Spot Exchanges Volume Data", "Let's check the cryptocurrency spot exchanges' volume data. I decided to check \
               spot exchanges' volume data because they represent how active the cryptocurrency market \
               is. Spot trading volume data is also more accurate regarding actual market activity. \
               I included well-known big names for spot trading activities, including Binance, \
               Coinbase, Kraken, OKX, etc."),

        (fig6, "Lightning Network (LN) Data", "Now, let's analyze the Lightning Network (LN) data. Many cryptocurrency advocates \
               believe that LN will have to be widely adopted sooner or later if we want to see Bitcoin's \
                   mainstream adoption due to its much lower fees. When it comes to LN, the more capacity \
                       the network has, the more value it can transfer at any given time without needing to \
                           open new channels. As for channel count, a higher channel count suggests a more \
                               interconnected and potentially more decentralized network. Unfortunately, \
                                   both numbers have not changed much. These numbers may potentially change \
                                       in the bull market, though.")  
    )
], id='main-container')

