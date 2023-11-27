"""
Dash App
"""

### Import Libraries
import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html

def format_title(words):
    if words == "Home":
        return words

    word = words.split()
    if len(word) > 0:
        word[0] = word[0].upper()
        word[1] = word[1].title()
    return " ".join(word)


def sidebar_menu():
    btc_pages = [page for page in dash.page_registry.values() if 'BTC' in page['title']]
    eth_pages = [page for page in dash.page_registry.values() if 'ETH' in page['title']]
    bnb_pages = [page for page in dash.page_registry.values() if 'BNB' in page['title']]
    other_pages = [page for page in dash.page_registry.values() if page not in btc_pages \
                   and page not in eth_pages and page not in bnb_pages]

    return html.Div([
        html.H3('Explore'),
        # Links
        html.Div([
            # Internal Pages
            html.Div([
                dcc.Link(
                    format_title(page['name']),
                    href=page["relative_path"],
                    className='menu-link'
                ) for page in other_pages
            ]),
            dbc.DropdownMenu(
                label="Bitcoin",
                children=[
                    dbc.DropdownMenuItem(
                        format_title(page['name'].replace('BTC ', '')),
                        href=page["relative_path"],
                    ) for page in btc_pages
                ],
                className='menu-link',
                nav=True
            ),
            dbc.DropdownMenu(
                label="Ethereum",
                children=[
                    dbc.DropdownMenuItem(
                        format_title(page['name'].replace('ETH ', '')),
                        href=page["relative_path"],
                    ) for page in eth_pages
                ],
                className='menu-link',
                nav=True
            ),
            dbc.DropdownMenu(
                label="BNB",
                children=[
                    dbc.DropdownMenuItem(
                        format_title(page['name'].replace('BNB ', '')),
                        href=page["relative_path"],
                    ) for page in bnb_pages
                ],
                className='menu-link',
                nav=True
            ),
            # External link
            html.A(
                'Deftify Beta',
                href='https://beta.deftify.io',
                className='menu-link',
                target='_blank'
            ),
        ], className='menu-container')
    ], id='sidebar')


# Use Multi-Pages
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Deftify Monthly Cryptocurrency Analysis"

app.layout = html.Div([
    dash.page_container
])

# Run the App - use the first two lines below for local testing
# if __name__ == '__main__':
#     app.run_server(debug=True, dev_tools_hot_reload=False)

if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=False, host='0.0.0.0', port=10000)
