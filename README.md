# Bitcoin Analysis with Plotly and Dash

Welcome to the GitHub repo for my analysis report web app on Bitcoin and other cryptocurrencies. You can check the web app here: [https://research.deftify.io/](https://research.deftify.io/)

This web app use Plotly for the data visualizations and Dash to build the web dashboard.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Explanation](#explanation)

## Installation

Use separate virtual environment. And then, install directly from requirements.txt
```
pip install -r requirements.txt
```

## Usage

Create config.ini and put your Owlracle API key, starts with `OWLRACTLE_API_KEY =`. After that, run:
```
python app.py
```

That's it! You will be able to run this web app in localhost.

## Explanation
`app.py` - This script is utilized to establish the web app using the Dash library. Since this is a multi-page Dash app, you can check the individual pages inside the **pages** folder. I also utilize the **app_layout** package for this app.

You may want to ask, why do we utilize Pickle files to create this web app? Because the Pickle files allow us to visualize the data offline. Otherwise, the web app will have to keep pulling API data from various sources, and that comes with a lot of limitations since I use free API sources to create those Pickle files in the first place.