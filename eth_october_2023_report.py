"""
Data Visualization and Dashboarding - Ethereum
"""

## Libraries

# import numpy as np
import pandas as pd

import dash
from dash import dcc, html
from dash import dash_table
from dash.dependencies import Input, Output, State

import plotly.express as px
import plotly.graph_objects as go


### Import Data, better to import from pickle files, rather than importing the script directly
eth_90d = pd.read_pickle('pickles/october_2023/eth_90d.pkl')
eth_gas_fee = pd.read_pickle('pickles/october_2023/eth_gas_fee.pkl')
eth_combined_data_final = pd.read_pickle('pickles/october_2023/eth_combined_data_final.pkl')
eth_tvl = pd.read_pickle('pickles/october_2023/eth_tvl.pkl')
eth_defi_tvl_top10 = pd.read_pickle('pickles/october_2023/eth_defi_tvl_top10.pkl')


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

# for fig1, ensure start_date is always earlier than end_date
default_start_date = min_date
default_end_date = max_date

if default_start_date > default_end_date:
    default_start_date, default_end_date = default_end_date, default_start_date


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
    title='Ethereum Top 10 DeFi - TVL Comparison (Past 3 Years)',
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


### Section 2: Define the App Layout
app = dash.Dash(__name__)
app.index_string = '''
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

app.layout = html.Div([
    # Sidebar
    html.Div([
        html.Br(), #a line break so the table will be aligned better
        html.Div([
            html.H4('Ethereum Data Table'),
            dash_table.DataTable(
                id='eth-data-table',
                columns=[{'name': col, 'id': col} for col in eth_combined_data_final.columns],
                data=eth_combined_data_final.to_dict('records'),
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
        html.H1("Ethereum (ETH) October 2023 Report", className="title_text", id="title_text_1"),
        html.H5("by: Ruddy Setiadi Gunawan", className="author_text", id="author_text_1"),

        html.H3("Key Insights:", className="heading_text", id="key_insight_heading"),

        html.Ul([
            html.Li("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod \
                    tempor incididunt ut labore et dolore magna aliqua."),
            html.Li("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod \
                    tempor incididunt ut labore et dolore magna aliqua."),
            html.Li("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod \
                    tempor incididunt ut labore et dolore magna aliqua.")
        ], className="bullet_points", id="bullet_points_list"),

        # First section with DatePickerRange and fig1
        html.Div([

            html.H2("Ethereum vs. Bitcoin Price Action", className="heading_text", \
                    id="heading_text_1"),

            html.P("You can choose the start and end dates below (the min. date is July 22nd, \
                   while max. date is October 22nd)", className="citation_text", \
                    id="citation_text_1_1"),

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

        html.P("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor \
               incididunt ut labore et dolore magna aliqua.", \
                    className="paragraph_text", id="paragraph_text_1_1"),

        html.P("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor \
               incididunt ut labore et dolore magna aliqua.", \
                   className="paragraph_text", id="paragraph_text_1_2"),

        html.P("P.S.: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod \
               tempor incididunt ut labore et dolore magna aliqua.", \
                   className="citation_text", id="citation_text_1_2"),
        ], className="section", id='section1'),

        # Second section with fig2
        html.Div([
    
            html.H2("Ethereum Gas Fees (GWEI)", className="heading_text", id="heading_text_2"),
    
            html.P("This section displays Ethereum gas fees in GWEI for the past 30 days", 
                   className="citation_text", id="citation_text_2_1"),
    
            dcc.Graph(id='eth-gas-fee-chart', figure=fig2, className='graph-bg-dark'),

        html.P("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor \
               incididunt ut labore et dolore magna aliqua.", \
                    className="paragraph_text", id="paragraph_text_2_1"),

        html.P("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor \
               incididunt ut labore et dolore magna aliqua.", \
           className="paragraph_text", id="paragraph_text_2_2"),

        html.P("P.S.: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod \
               tempor incididunt ut labore et dolore magna aliqua.", \
           className="citation_text", id="citation_text_2_2"),
        ], className="section", id='section2'),

        # Third section with fig3
        html.Div([
    
            html.H2("Ethereum TVL Historical Data (Past 3 Years)", className="heading_text", \
                    id="heading_text_3"),
    
            html.P("This section displays Ethereum TVL historical data in the past 3 years.", 
                   className="citation_text", id="citation_text_3_1"),
    
            dcc.Graph(id='time-series-chart-tvl', figure=fig3, className='graph-bg-dark'),

        html.P("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor \
               incididunt ut labore et dolore magna aliqua.", \
                   className="paragraph_text", id="paragraph_text_3_1"),

        html.P("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor \
               incididunt ut labore et dolore magna aliqua.", \
                   className="paragraph_text", id="paragraph_text_3_2"),

        html.P("P.S.: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod \
               tempor incididunt ut labore et dolore magna aliqua.", \
                   className="citation_text", id="citation_text_3_2"),
        ], className="section", id='section3'),

        # Fourth section with fig4
        html.Div([
    
            html.H2("Ethereum Top 10 DeFi - TVL Comparison (Past 3 Years)", className="heading_text", \
                    id="heading_text_4"),
    
            html.P("This section displays top 10 DeFi protocols for the Ethereum chain and compare \
                   their TVL historical data", 
                   className="citation_text", id="citation_text_4_1"),
    
            dcc.Graph(id='time-series-chart-tvl-top10', figure=fig4, className='graph-bg-dark'),

        html.P("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor \
               incididunt ut labore et dolore magna aliqua.", \
                   className="paragraph_text", id="paragraph_text_4_1"),

        html.P("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor \
               incididunt ut labore et dolore magna aliqua.", \
                   className="paragraph_text", id="paragraph_text_4_2"),

        html.P("P.S.: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod \
               tempor incididunt ut labore et dolore magna aliqua.", \
                   className="citation_text", id="citation_text_4_2"),
        ], className="section", id='section4'),

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
    """function to update the date widget"""
    # Ensure the provided start_date is always earlier than the end_date
    start_date = min(input_start_date, input_end_date)
    end_date = max(input_start_date, input_end_date)

    fig1_data_filtered = eth_90d[(eth_90d['Date'] >= start_date) & \
                                            (eth_90d['Date'] <= end_date)]

    fig1_trace1 = go.Scatter(x=fig1_data_filtered['Date'], y=fig1_data_filtered\
                             ['price_vs_btc'], mode='lines', name='eth', \
                                line={'color': 'green'})

    fig1_layout = go.Layout(
        height=400,
        plot_bgcolor='#2b2b2b',
        paper_bgcolor='#2b2b2b',
        title='ETH vs. BTC Price Action',
        titlefont={'color': 'white'},
        title_x=0.05,
        yaxis={
            'title': '',
            'gridcolor': '#636363',
            'zerolinecolor': '#636363',
            'tickfont': {'color': 'white'},
            'titlefont': {'color': 'white'}
        },
        xaxis={
            'gridcolor': '#636363',
            'zerolinecolor': '#636363',
            'tickfont': {'color': 'white'}
        },
        legend={'font': {'color': 'white'}}
    )

    fig = {"data": [fig1_trace1], "layout": fig1_layout}

    # Only adjust the date range if the callback's input dates are swapped
    if input_start_date != state_start_date or input_end_date != state_end_date:
        return fig, start_date, end_date
    else:
        return fig, state_start_date, state_end_date


### Run the app

# dev_tools_hot_reload set to false to prevent automatic refresh
# the first two lines below are for the localhost

if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=False)
# if __name__ == '__main__':
#     app.run_server(debug=True, dev_tools_hot_reload=False, host='0.0.0.0', port=10000)
