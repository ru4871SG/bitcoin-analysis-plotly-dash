"""
Dash App
"""

### Import Libraries
# app_layout package
import app_layout.sidebar as sidebar

import dash
from dash import Dash, dcc, html


def format_title(words):
    if words == "Home":
        return words

    word = words.split()
    if len(word) > 0:
        word[0] = word[0].upper()
        word[1] = word[1].title()
    return " ".join(word)


def sidebar_menu(data_table):
    return html.Div([
        html.H3('Explore'),
        # Links
        html.Div([
            # Internal Pages
            dcc.Link(
                format_title(page['name']),
                href=page["relative_path"],
                className='menu-link'
            ) for page in dash.page_registry.values()
        ]
        , className='menu-container'),

        # Data Table
        html.H3('Data Table'),
        sidebar.generate(data_table)
    ], id='sidebar')


# Use Multi-Pages
app = Dash(__name__, use_pages=True)

app.layout = html.Div([
    dash.page_container
])

# Run the App - use the first two lines below for local testing
# if __name__ == '__main__':
#     app.run_server(debug=True, dev_tools_hot_reload=False)

if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=False, host='0.0.0.0', port=10000)
