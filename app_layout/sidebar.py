from dash import dash_table

def generate(data_table):
    return dash_table.DataTable(
        id='data-table',
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
