## Libraries

# import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

import dash
from dash import dcc, html
from dash import dash_table
from dash.dependencies import Input, Output, State

import plotly.express as px
import plotly.graph_objects as go


### Import Data, better to import from pickle files, rather than importing the script directly
btc_90d_w_external = pd.read_pickle('btc_90d_w_external.pkl')
mempool_stats_30d_grouped = pd.read_pickle('mempool_stats_30d_grouped.pkl')
btc_mining_pools = pd.read_pickle('btc_mining_pools.pkl')
btc_combined_data_final = pd.read_pickle('btc_combined_data_final.pkl')
spot_exchanges_volume = pd.read_pickle('spot_exchanges_volume.pkl')
lightning_mempool_total_capacity = pd.read_pickle('lightning_mempool_total_capacity.pkl')

def format_value(data, value):
    conditions = [
        "market cap", "fully diluted valuation",
        "ATH", "ATL"
    ]
    
    if data in conditions:
        return "${:,.0f}".format(value)
    elif data in ["max supply", "circulating supply", "twitter followers", "github forks", "github stars",\
                  "github subscribers"]:
        return "{:,.0f}".format(value)
    return value

btc_combined_data_final['Value'] = btc_combined_data_final.apply(lambda row: \
                                        format_value(row['Data'], row['Value']), axis=1)

### Section 1: Define the Plots Using Plotly

## fig1: Bitcoin's Line Chart, with NDX and Gold (Normalized)
# define fig1
min_date = min(btc_90d_w_external['Date'])
max_date = max(btc_90d_w_external['Date'])

fig1_data_filtered = btc_90d_w_external[(btc_90d_w_external['Date'] >= max_date - pd.Timedelta(days=90)) & 
                                   (btc_90d_w_external['Date'] <= max_date)]
    
fig1_trace1 = go.Scatter(x=fig1_data_filtered['Date'], y=fig1_data_filtered['btc_price_normalized'], 
                    mode='lines', name='BTC', line=dict(color='green'))
    
fig1_trace2 = go.Scatter(x=fig1_data_filtered['Date'], y=fig1_data_filtered['ndx_price_normalized'], 
                    mode='lines', name='NASDAQ 100', line=dict(color='red'))
    
fig1_trace3 = go.Scatter(x=fig1_data_filtered['Date'], y=fig1_data_filtered['gold_price_normalized'], 
                    mode='lines', name='Gold', line=dict(color='gold'))
    
fig1_layout = go.Layout(height=400, 
                   title='BTC vs. NDX vs. Gold - Normalized',
                   titlefont=dict(color='white'),
                   title_x=0.05,
                   yaxis=dict(title=''))
    
fig1 = {"data": [fig1_trace1, fig1_trace2, fig1_trace3], "layout": fig1_layout}

fig1_layout = go.Layout(
    height=400,
    plot_bgcolor='#2b2b2b',
    paper_bgcolor='#2b2b2b',
    yaxis=dict(
        gridcolor='#636363',
        zerolinecolor='#636363',
        tickfont=dict(color='white'),
        titlefont=dict(color='white')
    ),
    xaxis=dict(
        gridcolor='#636363',
        zerolinecolor='#636363',
        tickfont=dict(color='white')
    ),
    legend=dict(font=dict(color='white'))
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
fig2.add_trace(go.Scatter(x=btc_90d_w_external_and_months["btc_price_normalized"], 
                     y=y_pred, mode='lines', 
                     name='Trend Line', line=dict(color='blue')))

fig2_layout = fig2.layout

fig2_layout.update(
    height=400,
    plot_bgcolor='#2b2b2b', 
    paper_bgcolor='#2b2b2b',
    yaxis=dict(
        gridcolor='#636363',
        zerolinecolor='#636363',
        tickfont=dict(color='white'),
        titlefont=dict(color='white')
    ),
    xaxis=dict(
        gridcolor='#636363',
        zerolinecolor='#636363',
        tickfont=dict(color='white'),
        titlefont=dict(color='white')
    ),
    legend=dict(font=dict(color='white')),
    title_font=dict(color='white')
)

fig2 = {"data": fig2.data, "layout": fig2_layout}


## fig3: Bitcoin Median Tx Fee Over Time
# define fig3
fig3 = px.bar(mempool_stats_30d_grouped, x="block_group", y="medianFee", 
              title="Bitcoin Median Tx Fee Over Time", 
              color_discrete_sequence=['#a2823c'],
              hover_data={"block_group": False, "medianFee": False}, # To exclude default hovertemplate info
              custom_data=['block_group', 'medianFee', 'height']) #include custom_data for the new hovertemplate

fig3.update_traces(hovertemplate="<b>Block Height Group:</b> %{customdata[0]}<br>\
            <b>Median Fee:</b> %{customdata[1]:.0f} sat/vB<br><b>End of Block Height:</b> %{customdata[2]:.0f}")

# Set the x-axis label, y-axis label and adjust the x-axis tick angle
fig3.update_layout(
    yaxis=dict(
        gridcolor='#636363',
        zerolinecolor='#636363',
        tickfont=dict(color='white'),
        titlefont=dict(color='white')
    ),
    xaxis=dict(
        gridcolor='#636363',
        zerolinecolor='#636363',
        tickfont=dict(color='white'),
        titlefont=dict(color='white')
    ),
    plot_bgcolor='#2b2b2b',
    paper_bgcolor='#2b2b2b',
    legend=dict(font=dict(color='white')),
    title_font=dict(color='white')
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

# Define fig4
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
    textfont=dict(color='white')
)

# Set the x-axis label, y-axis label and adjust the x-axis tick angle
fig4.update_layout(
    yaxis=dict(
        gridcolor='#636363',
        zerolinecolor='#636363',
        tickfont=dict(color='white'),
        titlefont=dict(color='white')
    ),
    xaxis=dict(
        gridcolor='#636363',
        zerolinecolor='#636363',
        tickfont=dict(color='white'),
        titlefont=dict(color='white')
    ),
    plot_bgcolor='#2b2b2b',
    paper_bgcolor='#2b2b2b',
    legend=dict(font=dict(color='white')),
    title_font=dict(color='white')
)


## fig5: Exchange Data (Spot)

# define fig5
# Create the traces for each exchange
trace1 = go.Scatter(x=spot_exchanges_volume['date'], y=spot_exchanges_volume['binance_vol_in_btc'],
                    mode='lines', name='Binance',
                    text=["<b>Exchange: Binance</b><br>Trading Vol.: {:,.2f} BTC<br>Date: {}".format(vol, date) for vol, date in zip(spot_exchanges_volume['binance_vol_in_btc'], spot_exchanges_volume['date'])],
                    hoverinfo='text')
trace2 = go.Scatter(x=spot_exchanges_volume['date'], y=spot_exchanges_volume['gdax_vol_in_btc'],
                    mode='lines', name='Coinbase',
                    text=["<b>Exchange: Coinbase</b><br>Trading Vol.: {:,.2f} BTC<br>Date: {}".format(vol, date) for vol, date in zip(spot_exchanges_volume['gdax_vol_in_btc'], spot_exchanges_volume['date'])],
                    hoverinfo='text')
trace3 = go.Scatter(x=spot_exchanges_volume['date'], y=spot_exchanges_volume['kraken_vol_in_btc'],
                    mode='lines', name='Kraken',
                    text=["<b>Exchange: Kraken</b><br>Trading Vol.: {:,.2f} BTC<br>Date: {}".format(vol, date) for vol, date in zip(spot_exchanges_volume['kraken_vol_in_btc'], spot_exchanges_volume['date'])],
                    hoverinfo='text')
trace4 = go.Scatter(x=spot_exchanges_volume['date'], y=spot_exchanges_volume['kucoin_vol_in_btc'],
                    mode='lines', name='Kucoin',
                    text=["<b>Exchange: Kucoin</b><br>Trading Vol.: {:,.2f} BTC<br>Date: {}".format(vol, date) for vol, date in zip(spot_exchanges_volume['kucoin_vol_in_btc'], spot_exchanges_volume['date'])],
                    hoverinfo='text')
trace5 = go.Scatter(x=spot_exchanges_volume['date'], y=spot_exchanges_volume['bitstamp_vol_in_btc'],
                    mode='lines', name='Bitstamp',
                    text=["<b>Exchange: Bitstamp</b><br>Trading Vol.: {:,.2f} BTC<br>Date: {}".format(vol, date) for vol, date in zip(spot_exchanges_volume['bitstamp_vol_in_btc'], spot_exchanges_volume['date'])],
                    hoverinfo='text')
trace6 = go.Scatter(x=spot_exchanges_volume['date'], y=spot_exchanges_volume['okex_vol_in_btc'],
                    mode='lines', name='OKX',
                    text=["<b>Exchange: OKX</b><br>Trading Vol.: {:,.2f} BTC<br>Date: {}".format(vol, date) for vol, date in zip(spot_exchanges_volume['okex_vol_in_btc'], spot_exchanges_volume['date'])],
                    hoverinfo='text')
trace7 = go.Scatter(x=spot_exchanges_volume['date'], y=spot_exchanges_volume['bitfinex_vol_in_btc'],
                    mode='lines', name='Bitfinex',
                    text=["<b>Exchange: Bitfinex</b><br>Trading Vol.: {:,.2f} BTC<br>Date: {}".format(vol, date) for vol, date in zip(spot_exchanges_volume['bitfinex_vol_in_btc'], spot_exchanges_volume['date'])],
                    hoverinfo='text')
trace8 = go.Scatter(x=spot_exchanges_volume['date'], y=spot_exchanges_volume['huobi_vol_in_btc'],
                    mode='lines', name='Huobi',
                    text=["<b>Exchange: Huobi</b><br>Trading Vol.: {:,.2f} BTC<br>Date: {}".format(vol, date) for vol, date in zip(spot_exchanges_volume['huobi_vol_in_btc'], spot_exchanges_volume['date'])],
                    hoverinfo='text')
trace9 = go.Scatter(x=spot_exchanges_volume['date'], y=spot_exchanges_volume['gemini_vol_in_btc'],
                     mode='lines', name='Gemini',
                     text=["<b>Exchange: Gemini</b><br>Trading Vol.: {:,.2f} BTC<br>Date: {}".format(vol, date) for vol, date in zip(spot_exchanges_volume['gemini_vol_in_btc'], spot_exchanges_volume['date'])],
                     hoverinfo='text')

# Create the layout for the chart
layout_fig5 = go.Layout(title='Trading Volumes of Spot Exchanges',
                   xaxis=dict(title='Date'),
                   yaxis=dict(title='Volume in BTC'))

# Create the figure and add the traces and layout
fig5 = go.Figure(data=[trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace8, trace9], \
                 layout=layout_fig5)

# Set the x-axis label, y-axis label and adjust the x-axis tick angle, and the colors too
fig5.update_layout(
    yaxis=dict(
        gridcolor='#636363',
        zerolinecolor='#636363',
        tickfont=dict(color='white'),
        titlefont=dict(color='white')
    ),
    xaxis=dict(
        gridcolor='#636363',
        zerolinecolor='#636363',
        tickfont=dict(color='white'),
        titlefont=dict(color='white')
    ),
    plot_bgcolor='#2b2b2b',
    paper_bgcolor='#2b2b2b',
    legend=dict(font=dict(color='white')),
    title_font=dict(color='white')
)


## fig6: Lightning Network Stats
# define fig6
trace1 = go.Scatter(x=lightning_mempool_total_capacity['added'], 
                    y=lightning_mempool_total_capacity['total_capacity'],
                    mode='lines', 
                    name='Total Capacity', 
                    yaxis='y1',
                    text=['Total Capacity: {:.0f}'.format(val) for val in lightning_mempool_total_capacity['total_capacity']],
                    hoverinfo='text+y+x',
                    hovertemplate='<b>%{text}</b><br>' + '<b>Date</b>: %{x}<extra></extra>')

trace2 = go.Scatter(x=lightning_mempool_total_capacity['added'], 
                    y=lightning_mempool_total_capacity['channel_count'],
                    mode='lines', 
                    name='Channel Count', 
                    yaxis='y2',
                    text=['Channel Count: {:.0f}'.format(val) for val in lightning_mempool_total_capacity['channel_count']],
                    hoverinfo='text+y+x',
                    hovertemplate='<b>%{text}</b><br>' + '<b>Date</b>: %{x}<extra></extra>')

# Create the layout for the chart
layout_fig6 = go.Layout(title='Mempool Stats - Lightning Network',
                   xaxis=dict(title='Date'),
                   yaxis=dict(title='Total Capacity', side='left', showgrid=False),
                   yaxis2=dict(title='Channel Count', side='right', overlaying='y', 
                               showgrid=False, titlefont=dict(color='white'), tickfont=dict(color='white')))

# Create the figure and add the traces and layout
fig6 = go.Figure(data=[trace1, trace2], layout=layout_fig6)

# Set the x-axis label, y-axis label and adjust the x-axis tick angle, and the colors too
fig6.update_layout(
    yaxis=dict(
        gridcolor='#636363',
        zerolinecolor='#636363',
        tickfont=dict(color='white', size=8),
        titlefont=dict(color='white')
    ),
    yaxis2=dict(
    gridcolor='#636363',
    zerolinecolor='#636363',
    tickfont=dict(color='white', size=8),
    titlefont=dict(color='white')
    ),
    xaxis=dict(
        gridcolor='#636363',
        zerolinecolor='#636363',
        tickfont=dict(color='white', size=10),
        titlefont=dict(color='white')
    ),
    plot_bgcolor='#2b2b2b',
    paper_bgcolor='#2b2b2b',
    legend=dict(font=dict(color='white')),
    title_font=dict(color='white')
)


### Section 2: Define the App Layout

app = dash.Dash(__name__)

# Modify the default index string's title
app.index_string = '''
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

# for fig1, ensure start_date is always earlier than end_date
default_start_date = min_date
default_end_date = max_date

if default_start_date > default_end_date:
    default_start_date, default_end_date = default_end_date, default_start_date

# for fig2, define the options for the y-axis dropdown
y_axis_options = [{'label': 'NDX', 'value': 'ndx_price_normalized'},
                  {'label': 'Gold', 'value': 'gold_price_normalized'}]

# Define the layout
app.layout = html.Div([
    # Sidebar with corrected color and full height
    html.Div([
        html.Br(), #a line break so the table will be aligned better
        html.Div([
            html.H4('Bitcoin Data Table'),
            dash_table.DataTable(
                id='btc-data-table',
                columns=[{'name': col, 'id': col} for col in btc_combined_data_final.columns],
                data=btc_combined_data_final.to_dict('records'),
                style_table={
                    'overflowX': 'scroll',
                    'width': '90%',
                    'border': '1px solid #ccc',
                    'margin': 'auto'
                },
                style_header={
                    'backgroundColor': '#2b2b2b',
                    'fontWeight': 'bold',
                    'color': 'white'
                },
                style_cell={
                    'backgroundColor': '#3d3d3d',
                    'color': 'white',
                    'textAlign' : 'left'
                },
                page_action='none'
            )
        ], id='data-table')
    ], id='sidebar'),

     # Main Pane with multiple sections (boxes)
    html.Div([
        html.H1("Bitcoin (BTC) September 2023 Report", className="title_text", id="title_text_1"),
        html.H5("by: Ruddy Setiadi Gunawan", className="author_text", id="author_text_1"),
        
        html.H3("Key Insights:", className="heading_text", id="key_insight_heading"),
        
        html.Ul([
            html.Li("In Q3 2023, Bitcoin price action has not been tightly correlated to NDX or Gold"),
            html.Li("In the month of September, Bitcoin median tx fee were usually low, peaked at 29 sat/vB"),
            html.Li("Foundry USA and AntPool are still leading the mining pool distribution"),
            html.Li("Binance is still leading the spot trading volume data, with peak activities around July 14th and August 18th"),
            html.Li("Lightning Network stats have been stagnant in the past 3 months")
        ], className="bullet_points", id="bullet_points_list"), 
        # First section with DatePickerRange and fig1
        html.Div([

            html.H2("Bitcoin Price Action vs. NDX and Gold", className="heading_text", id="heading_text_1"),

            html.P("You can choose the start and end dates below (the min. date is July 5th, \
                   while max. date is September 28th)", className="citation_text", id="citation_text_1_1"),
                        
            dcc.DatePickerRange(
                id='custom-date-picker',
                min_date_allowed=min_date,
                max_date_allowed=max_date,
                start_date=default_start_date,
                end_date=default_end_date,
                display_format="MMM D",
                end_date_placeholder_text="End Date",
                start_date_placeholder_text="Start Date"
            ),

            dcc.Graph(id='time-series-chart', figure=fig1, className='graph-bg-dark'),
            
        html.P("Many people love to compare Bitcoin price action with NASDAQ 100 (NDX) and Gold. \
               Since all three are heavily affected by external factors (e.g., by the Fed's interest rate \
               policies), it's interesting to see how correlated they are. This section explains the \
                price action movements for Bitcoin, NDX, and Gold with actual data. Bitcoin price often \
                followed NDX price action in the past, but it's been a bit different recently.", 
               className="paragraph_text", id="paragraph_text_1_1"),

        html.P("The above chart normalized the starting prices of the three objects (BTC, NDX, and \
             Gold) to make it easier to see their correlation. As you can see in the above chart, \
            Bitcoin has been underperforming in the past 3 months compared to NDX and Gold. \
                On August 16th, Bitcoin suffered a heavy bearish pressure, and it never \
                    really recovered ever since. Meanwhile, NDX and Gold have been much more \
                        stable compared to Bitcoin. It remains to be seen whether Bitcoin price action \
                            will eventually follow NDX or Gold again",
           className="paragraph_text", id="paragraph_text_1_2"),
                
        html.P("P.S.: July 3rd and July 4th data were omitted because the U.S. stock market closed early \
               on July 3rd, and was fully closed on July 4th. The dates above followed the U.S. stock \
                   market open days for chart consistency.",
           className="citation_text", id="citation_text_1_2"),
        ], className="section", id='section1'),

        # Second section with y-axis dropdown and fig2
        html.Div([

            html.H2("Correlation Analysis: Bitcoin vs. NDX and Gold", className="heading_text", id="heading_text_2"),

            html.P("You can choose the y-axis (between NDX and Gold) for the scatter plot below", \
                   className="citation_text", id="citation_text_2"),
                
            html.Div([
                html.P("Choose the y-axis. BTC vs. ", className="paragraph_text", id="text_pre_dropdown_1"),
                dcc.Dropdown(
                    id='y-axis-dropdown',
                    options=y_axis_options,
                    value='ndx_price_normalized',
                    clearable=False,
                    searchable=False,
                    className='dropdown-width'
                ),
            ], className='flex-center'),

            dcc.Graph(id='scatter-chart'),
            
        html.P("Our second analysis used scatter plots to determine the correlation between Bitcoin vs. \
               NDX and Bitcoin vs. Gold. Both scatter plots show moderate correlation, although they are not \
                   tightly correlated. I have also included the linear regression (trend) line so you can \
                       see for yourself how closely related the x-axis and y-axis are.", 
               className="paragraph_text", id="paragraph_text_2_1"),
            
        html.P("The first two data visualizations above show that Bitcoin's price action is not as consistent \
               as Gold and NDX. While more volatility is already expected from Bitcoin, past trends have \
                   typically shown similar trends (at least between Bitcoin and NDX). In contrast, the \
                       current trend no longer offers the same direction. However, many experts predict \
                           that they may become closely correlated again when the Fed starts to lower the \
                               interest rate in the U.S.", 
               className="paragraph_text", id="paragraph_text_2_2"),
        ], className="section", id='section2'),

        # Third section with fig3
        html.Div([

            html.H2("Bitcoin Block Analysis - Median Tx Fee", className="heading_text", id="heading_text_3"),
            dcc.Graph(id='mempool-stats-chart', figure=fig3, className='graph-bg-dark'),
            
        html.P("Now, let’s check the Bitcoin block data directly from mempool to see the median transaction \
               (tx) fee for the past 30 days. I used mempool’s data because it is a widely trusted blockchain \
                   explorer in the Bitcoin community. Looks like the median tx fees have not fluctuated much \
                       in the past 30 days. Around September 19th (end of the block height 808519), \
                           the median transaction fee peaked at 29 sat/vB, but it’s been trending down ever \
                            since, signaling a lack of trading activities in the Bitcoin blockchain.\
                            To analyze the median tx fee, I grouped every 144 blocks into just one \
                            block group. On average, Bitcoin mines 144 blocks per day.", 
               className="paragraph_text", id="paragraph_text_3_1"),
            
        html.P("Disclaimer: Because of the variance in hashing power on the network, the number 144 \
               is just a target.", 
               className="citation_text", id="citation_text_3_1"),
        ], className="section", id='section3'),

        # Fourth section with fig4
        html.Div([

            html.H2("Bitcoin Mining Pools", className="heading_text", id="heading_text_4"),

            dcc.Graph(id='mining-pool-pie-chart', figure=fig4, className='graph-bg-dark'),
            
            html.P("This section analyzes Bitcoin mining pools' distribution from mempool. Foundry USA \
                   and AntPool are still leading the distribution, with F2Pool, ViaBTC, and BinancePool \
                       following behind them closely. The mining pools' distribution in the Bitcoin \
                           network is well diversified, as you can see from the pie chart above, and it's \
                               much more decentralized than most altcoins in the cryptocurrency industry.", 
                   className="paragraph_text", id="paragraph_text_4_1"),
        ], className="section", id='section4'),

        # Fifth section with fig5
        html.Div([

            html.H2("Spot Exchanges Volume Data", className="heading_text", id="heading_text_5"),

            dcc.Graph(id='exchange-data-spot', figure=fig5, className='graph-bg-dark'),
            
        html.P("Now, let’s check the cryptocurrency spot exchanges' volume data. I decided to check spot \
               exchanges’ volume data because they represent how active the cryptocurrency market is. Spot \
                   trading volume data is also more accurate regarding actual market activity. I included \
                       well-known big names for spot trading activities, including Binance, Coinbase, \
                           Kraken, OKX, etc.", 
               className="paragraph_text", id="paragraph_text_5_1"),
            
        html.P("The above chart shows that Binance still dominates the market as always, with peak \
               activities around July 14th and August 18th. Even in the last days of September, Binance's \
                   trading volume still surpassed 133K Bitcoin per day. These details are essential because \
                       they show that there are still a lot of crypto day traders, even in the bear market. \
                           When analyzing Bitcoin, it’s necessary to see the overall health of the crypto \
                               market because Bitcoin dominates this industry, especially in the bear market.", 
               className="paragraph_text", id="paragraph_text_5_2"),
        ], className="section", id='section5'),

        # Sixth section with fig6
        html.Div([

            html.H2("Lightning Network (LN) Data", className="heading_text", id="heading_text_6"),

           dcc.Graph(id='lightning-network-stats', figure=fig6, className='graph-bg-dark'),
            
        html.P("Lastly, let’s analyze the Lightning Network (LN) data. Many cryptocurrency advocates \
               believe that LN will have to be widely adopted sooner or later if we want to see Bitcoin's \
                   mainstream adoption due to its much lower fees. When it comes to LN, the more capacity \
                       the network has, the more value it can transfer at any given time without needing to \
                           open new channels. As for channel count, a higher channel count suggests a more \
                               interconnected and potentially more decentralized network. Unfortunately, \
                                   both numbers have not changed much. These numbers may potentially change \
                                       in the bull market, though.", 
               className="paragraph_text", id="paragraph_text_6_1"),
            
        html.Br(),    
        ], className="section", id='section6'),
    ], id='main-pane')
], id='main-container')



### Section 3: Visualization Update Callbacks (App Callbacks)

## fig1 plot update function
@app.callback(
    [Output('time-series-chart', 'figure'),
     Output('custom-date-picker', 'start_date'),
     Output('custom-date-picker', 'end_date')],
    [Input('custom-date-picker', 'start_date'),
     Input('custom-date-picker', 'end_date')],
    [State('custom-date-picker', 'start_date'),
     State('custom-date-picker', 'end_date')]
)
def update_time_series_chart(input_start_date, input_end_date, state_start_date, state_end_date):
    
    # Ensure the provided start_date is always earlier than the end_date
    start_date = min(input_start_date, input_end_date)
    end_date = max(input_start_date, input_end_date)

    fig1_data_filtered = btc_90d_w_external[(btc_90d_w_external['Date'] >= start_date) & 
                                           (btc_90d_w_external['Date'] <= end_date)]
    
    fig1_trace1 = go.Scatter(x=fig1_data_filtered['Date'], y=fig1_data_filtered['btc_price_normalized'], 
                             mode='lines', name='BTC', line=dict(color='green'))
    
    fig1_trace2 = go.Scatter(x=fig1_data_filtered['Date'], y=fig1_data_filtered['ndx_price_normalized'], 
                             mode='lines', name='NASDAQ 100', line=dict(color='red'))
    
    fig1_trace3 = go.Scatter(x=fig1_data_filtered['Date'], y=fig1_data_filtered['gold_price_normalized'], 
                             mode='lines', name='Gold', line=dict(color='gold'))
    
    fig1_layout = go.Layout(
        height=400,
        plot_bgcolor='#2b2b2b',
        paper_bgcolor='#2b2b2b',
        title='BTC, NDX, and Gold Price - Normalized',
        titlefont=dict(color='white'),
        title_x=0.05,
        yaxis=dict(
            title='',
            gridcolor='#636363',
            zerolinecolor='#636363',
            tickfont=dict(color='white'),
            titlefont=dict(color='white')
        ),
        xaxis=dict(
            gridcolor='#636363',
            zerolinecolor='#636363',
            tickfont=dict(color='white')
        ),
        legend=dict(font=dict(color='white'))
    )

    fig = {"data": [fig1_trace1, fig1_trace2, fig1_trace3], "layout": fig1_layout}

    # Only adjust the date range if the callback's input dates are swapped
    if input_start_date != state_start_date or input_end_date != state_end_date:
        return fig, start_date, end_date
    else:
        return fig, state_start_date, state_end_date


## fig2 plot update function
y_axis_labels = {
        'ndx_price_normalized': 'NDX',
        'gold_price_normalized': 'GOLD'
    }

@app.callback(
    Output('scatter-chart', 'figure'),
     Input('y-axis-dropdown', 'value')  # Add the y-axis dropdown as an input
)
def update_scatter_chart(y_axis_variable):
    fig2_data = btc_90d_w_external_and_months

    y_axis_label = y_axis_labels.get(y_axis_variable, "UNKNOWN")
    
    # Compute linear regression line using sklearn
    X = fig2_data["btc_price_normalized"].values.reshape(-1, 1)
    y = fig2_data[y_axis_variable].values
    model = LinearRegression().fit(X, y)
    y_pred = model.predict(X)
    
    # Update the y-axis label based on the selected variable
    fig2 = px.scatter(fig2_data, x='btc_price_normalized', 
                    y=y_axis_variable, 
                    color='Month',
                    labels={'btc_price_normalized': 'BTC', 
                            y_axis_variable: y_axis_label}, 
                    title=f'BTC vs. {y_axis_label} - Normalized')
    
    # Add linear regression line (Trend Line) to the scatter plot
    fig2.add_trace(go.Scatter(x=fig2_data["btc_price_normalized"], 
                              y=y_pred, mode='lines', 
                              name='Trend Line', line=dict(color='#a2823c')))
    
    # Update layout properties 
    fig2.update_layout(
        height=400,
        plot_bgcolor='#2b2b2b',
        paper_bgcolor='#2b2b2b',
        yaxis=dict(
            gridcolor='#636363',
            zerolinecolor='#636363',
            tickfont=dict(color='white'),
            titlefont=dict(color='white')
        ),
        xaxis=dict(
            gridcolor='#636363',
            zerolinecolor='#636363',
            tickfont=dict(color='white'),
            titlefont=dict(color='white')
        ),
        legend=dict(font=dict(color='white')),
        title_font=dict(color='white')
    )

    fig2 = {"data": fig2.data, "layout": fig2.layout} 
    return fig2


### Run the app

# dev_tools_hot_reload set to false to prevent automatic refresh
# the first two lines below are for the localhost

# if __name__ == '__main__':
#     app.run_server(debug=True, dev_tools_hot_reload=False) 
if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=False, host='0.0.0.0', port=10000)
