from dash import dcc, dash_table, html


def generate(data_table):
    return html.Div([
        html.Br(),  # a line break for better alignment
        html.Div([
            html.H4('Data Table'),
            dash_table.DataTable(
                id='btc-data-table',
                columns=[{'name': col, 'id': col} for col in data_table.columns],
                data=data_table.to_dict('records'),
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
                    'textAlign': 'left'
                },
                page_action='none'
            )
        ], id='data-table')
    ], id='sidebar')
