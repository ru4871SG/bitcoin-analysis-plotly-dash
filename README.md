# Bitcoin Analysis with Plotly and Dash

Welcome to the GitHub repo for my analysis reports on Bitcoin and other cryptocurrencies. You can check the web app on Render.com: [https://bitcoin-analysis-dash.onrender.com](https://bitcoin-analysis-dash.onrender.com)

These analysis reports use the plotly library for the data visualizations and the dash library for the web app.

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

That's it! You will be able to run the web app in localhost.

## Explanation
There are different Python scripts that you can check in this repo:

`btc_script.py` - This is the ETL (Extract, Transform, Load) script for Bitcoin data. It is used to pull and transform data from three different API sources (CoinGecko, MemPool, and Yahoo Finance). The Pickle files are the automatic result of this script's operation (check the **pickles** folder).

`eth_script.py` - This is the ETL script for Ethereum data. It is used to pull and transform data from three different API sources (CoinGecko, Owlracle, and DefiLlama). The Pickle files are the automatic result of this script's operation (check the **pickles** folder).

`bnb_script.py` - This is the ETL script for BNB data. It is used to pull and transform data from three different API sources (CoinGecko, Owlracle, and DefiLlama). The Pickle files are the automatic result of this script's operation (check the **pickles** folder).

`app.py` - This script is utilized to establish the web app using the Dash library. Since this is a multi-page Dash app, you can check the individual pages inside the **pages** folder. I also utilize the **app_layout** package for this app.

You may want to ask, why do we need the Pickle files? Because otherwise the visualizations will have to keep pulling API data, and that's not good since I use free API sources with a lot of limitations.

Note: When you run `btc_script.py`, `eth_script.py`, or `bnb_script.py`, the Pickle files will be stored in "unassigned" subfolder inside the **pickles** folder. You will have to manually move these files from "unassigned" into their respective months (for example: if you run the script by the end of October, you should move the Pickle files to the "october_2023" subfolder). I include the "unassigned" folder in .gitignore.
