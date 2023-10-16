"""
Data Import and Wrangling Steps - ethereum
"""

# %%

## Libraries
# import numpy as np
import configparser
import json
import pandas as pd
import requests


# %%

## Part 1: 90 days of Ethereum Data
response = requests.get("https://api.coingecko.com/api/v3/coins/ethereum/market_chart?vs_currency=usd&days=90&interval=daily", \
                        timeout=10)
content = response.content
data = json.loads(content)

eth_total_volumes_90d = pd.DataFrame(data['total_volumes'], columns=['time', 'vol_24h'])
eth_total_volumes_90d['vol_24h'] = eth_total_volumes_90d['vol_24h'].apply(lambda x: format(x, ','))
eth_total_volumes_90d['time'] = pd.to_datetime(eth_total_volumes_90d['time'] / 1000, unit='s',\
                                               origin='unix', utc=True)

eth_price_90d = pd.DataFrame(data['prices'], columns=['time', 'price'])
eth_price_90d['price'] = eth_price_90d['price'].apply(lambda x: format(x, ','))
eth_price_90d['time'] = pd.to_datetime(eth_price_90d['time'] \
                                       / 1000, unit='s', origin='unix', utc=True)

eth_marketcap_90d = pd.DataFrame(data['market_caps'], columns=['time', 'marketcap'])
eth_marketcap_90d['marketcap'] = eth_marketcap_90d['marketcap'].apply(lambda x: format(x, ','))
eth_marketcap_90d['time'] = pd.to_datetime(eth_marketcap_90d['time'] / 1000, unit='s', \
                                           origin='unix', utc=True)

# Get ETH/BTC price as well for comparison
response = requests.get("https://api.coingecko.com/api/v3/coins/ethereum/market_chart?vs_currency=btc&days=90&interval=daily", \
                        timeout=10)
content = response.content
data = json.loads(content)

eth_price_90d_vs_btc = pd.DataFrame(data['prices'], columns=['time', 'price'])
eth_price_90d_vs_btc['price'] = eth_price_90d_vs_btc['price'].apply(lambda x: format(x, ','))
eth_price_90d_vs_btc['time'] = pd.to_datetime(eth_price_90d_vs_btc['time'] \
                                       / 1000, unit='s', origin='unix', utc=True)

eth_price_90d_vs_btc.rename(columns={'price': 'price_vs_btc'}, inplace=True)


# Join market cap, price, volume, and price_vs_btc
eth_90d = eth_price_90d.merge(eth_marketcap_90d, on='time').merge(eth_total_volumes_90d, on='time')\
          .merge(eth_price_90d_vs_btc, on='time')

# Create date column on the merged dataframe
eth_90d['Date'] = eth_90d['time'].dt.date

end_date = eth_90d['Date'].max()
start_date = eth_90d['Date'].min()

# %%

## Part 2: Average Gas Fee History from Owlracle for the Past 30 Days
#  Documentation: https://owlracle.info/docs#endpoint-history

# Store the API key in config.ini and use your own API key over there.
config = configparser.ConfigParser()
config.read('config.ini')

API_KEY = config['DEFAULT']['OWLRACTLE_API_KEY']

response = requests.get(f"https://api.owlracle.info/v4/eth/history?apikey={API_KEY}&candles=30&timeframe=1440", \
                        timeout=10)

content = response.content
data = json.loads(content)

eth_gas_fee = pd.DataFrame(data['candles'], columns=['avgGas', 'gasPrice', 'samples', 'timestamp'])

# Unnest the 'gasPrice' column, and drop the original gasPrice column
eth_gas_fee[['gasPrice_open', 'gasPrice_close', 'gasPrice_low', \
             'gasPrice_high']] = eth_gas_fee['gasPrice'].apply(pd.Series)
eth_gas_fee.drop('gasPrice', axis=1, inplace=True)

# Convert the 'timestamp' column to a datetime format, then format the time column properly
eth_gas_fee['time'] = pd.to_datetime(eth_gas_fee['timestamp'])
eth_gas_fee['time'] = eth_gas_fee['time'].dt.strftime('%Y-%m-%d %H:%M:%S.%f')


# %%

## Part 3: Developers and Community Data
ethereum_details = requests.get("https://api.coingecko.com/api/v3/coins/ethereum?localization=false&tickers=true&market_data=false&community_data=true&developer_data=true&sparkline=true", \
                               timeout=10)
ethereum_details_data = ethereum_details.json()

# developers_data
eth_developers_data = {
    "commit_count_4_weeks": ethereum_details_data["developer_data"]["commit_count_4_weeks"],
    "forks": ethereum_details_data["developer_data"]["forks"],
    "stars": ethereum_details_data["developer_data"]["stars"],
    "subscribers": ethereum_details_data["developer_data"]["subscribers"]
}
eth_developers_df = pd.DataFrame([eth_developers_data])

# community_data
eth_community_data = ethereum_details_data["community_data"]
eth_community_df = pd.DataFrame(list(eth_community_data.items()), columns=["new_column", "V1"]).T
header = eth_community_df.iloc[0]
eth_community_df = eth_community_df[1:]
eth_community_df.columns = header
eth_community_df.reset_index(drop=True, inplace=True)

# combine developers and community data
eth_combined_data = pd.concat([eth_community_df[["twitter_followers"]], eth_developers_df], axis=1)

# rename columns and use melt to reshape the data frame
eth_combined_data.rename(columns={
    "forks": "github forks",
    "stars": "github stars",
    "subscribers": "github subscribers",
    "twitter_followers": "twitter followers"
}, inplace=True)

eth_combined_data = eth_combined_data.round(0).melt(var_name="Data", value_name="Value")


# %%

## Part 4: ethereum Stats

# Define an error handling function for clarity
def fetch_eth_stats():
    """function to fetch ethereum stats from CoinGecko API"""
    try:
        response = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=ethereum&order=market_cap_desc&per_page=100&page=1&sparkline=false&price_change_percentage=90d&locale=en", \
                                timeout=10)
        response.raise_for_status()

        data = response.json()

        if not data:
            print("Empty response from the API.")
            return None

        eth_stats = data[0]
        return eth_stats

    except requests.RequestException as req_exception:  # Catch any Request-related exceptions
        print(f"Error fetching data from API: {req_exception}")
        return None
    except (IndexError, TypeError, KeyError):
        print("Unexpected structure in API response or ethereum data not found.")
        return None

eth_stats = fetch_eth_stats()

if eth_stats is None:
    print("Failed to fetch ethereum stats.")
else:
    # Continue processing
    pass

# Selecting the required columns
columns = ["market_cap", "market_cap_rank", "fully_diluted_valuation", \
           "circulating_supply", "max_supply", "ath", "atl"]
eth_stats_1 = {col: eth_stats[col] for col in columns if col in eth_stats}

# Rename columns
column_rename = {
    "market_cap": "market cap",
    "market_cap_rank": "market cap rank",
    "fully_diluted_valuation": "fully diluted valuation",
    "circulating_supply": "circulating supply",
    "max_supply": "max supply",
    "ath": "ATH",
    "atl": "ATL"
}
eth_stats_1 = {column_rename[key] if key in column_rename \
               else key: value for key, value in eth_stats_1.items()}

# Converting the dictionary to DataFrame and then melt to reshape the data frame
eth_stats_cleaned = pd.DataFrame([eth_stats_1]).melt(var_name="Data", value_name="Value").round(0)

# Since we already created `eth_combined_data`, we can concatenate both DataFrames
eth_combined_data_final = pd.concat([eth_stats_cleaned, eth_combined_data], ignore_index=True)


# %%

## Part 5: Ethereum DeFi Historical TVL Data from DefiLlama
# Documentation: https://defillama.com/docs/api

response = requests.get("https://api.llama.fi/v2/historicalChainTvl/Ethereum", \
                        timeout=10)
content = response.content
data = json.loads(content)

eth_defi_tvl = pd.DataFrame(data)

# Fix the TVL value and time format (from UNIX)
eth_defi_tvl['tvl'] = eth_defi_tvl['tvl'].apply(lambda x: format(x, ','))
eth_defi_tvl['date'] = pd.to_datetime(eth_defi_tvl['date'], unit='s', origin='unix', utc=True)

# %%

## Part 6: Historical TVL Data by Protocol from DefiLlama (Only Top 10 Protocols from Ethereum)
# Documentation: https://defillama.com/docs/api
# List of top 10 DeFi protocol names
eth_defi_protocol_list_names = ["aave", "lido", "makerdao", "uniswap", "summer.fi", "instadapp", \
                                "compound", "rocket-pool", "curve-dex", "convex-finance"]

# Initialize an empty variable to store the result later
eth_defi_protocol_list = []

for protocol in eth_defi_protocol_list_names:
    response = requests.get(f"https://api.llama.fi/protocol/{protocol}", timeout=10)
    content = response.content
    data = json.loads(content)

    # Create a DataFrame and process the data
    eth_defi_tvl = pd.DataFrame(data['chainTvls']['Ethereum']['tvl'])

    # Fix the totalLiquidityUSD value and time format (from UNIX)
    eth_defi_tvl['totalLiquidityUSD'] = eth_defi_tvl['totalLiquidityUSD'].apply(lambda x: format(x, ','))
    eth_defi_tvl.rename(columns={'totalLiquidityUSD': f'totalLiquidity_{protocol}'}, inplace=True)

    eth_defi_tvl['date'] = pd.to_datetime(eth_defi_tvl['date'], unit='s', origin='unix', utc=True)
    eth_defi_tvl['date'] = eth_defi_tvl['date'].dt.strftime('%Y-%m-%d')

    eth_defi_protocol_list.append(eth_defi_tvl)

# Merge all dataframes on the 'date' column
eth_defi_tvl_top10 = eth_defi_protocol_list[0]
for df in eth_defi_protocol_list[1:]:
    eth_defi_tvl_top10 = pd.merge(eth_defi_tvl_top10, df, on='date', how='inner')

# %%

## Part 7: Exchanges (Spot) Data

# List of top exchanges
exchange_names = ["binance", "gdax", "kraken", "kucoin", "bitstamp", \
                  "okex", "bitfinex", "huobi", "gemini"]

# Initialize an empty variable to store the result later
spot_exchanges_volume = None

# Loop through top exchanges
for exchange in exchange_names:
    url = f"https://api.coingecko.com/api/v3/exchanges/{exchange}/volume_chart?days=90"
    details = requests.get(url, timeout=10)
    details_data = details.json()

    # Convert to dataframe
    volume = pd.DataFrame(details_data, columns=["timestamp", f"{exchange}_vol_in_eth"])

    # Fix UNIX time stamp, data type, and decimal numbers
    volume["timestamp"] = volume["timestamp"].astype(float)
    volume["date_with_hour"] = pd.to_datetime(volume["timestamp"], unit='ms', \
                                              origin='unix', utc=True)
    volume["date"] = volume["date_with_hour"].dt.date
    volume[f"{exchange}_vol_in_eth"] = volume[f"{exchange}_vol_in_eth"]
    volume = volume[["date", f"{exchange}_vol_in_eth"]]

    # Merge with the final dataframe
    if spot_exchanges_volume is None:
        spot_exchanges_volume = volume
    else:
        spot_exchanges_volume = pd.merge(spot_exchanges_volume, volume, on="date", how="left")

# Convert the volume columns to float64
spot_exchanges_volume['binance_vol_in_eth'] = spot_exchanges_volume['binance_vol_in_eth']\
                                          .astype('float64')
spot_exchanges_volume['gdax_vol_in_eth'] = spot_exchanges_volume['gdax_vol_in_eth']\
                                          .astype('float64')
spot_exchanges_volume['kraken_vol_in_eth'] = spot_exchanges_volume['kraken_vol_in_eth']\
                                          .astype('float64')
spot_exchanges_volume['kucoin_vol_in_eth'] = spot_exchanges_volume['kucoin_vol_in_eth']\
                                          .astype('float64')
spot_exchanges_volume['bitstamp_vol_in_eth'] = spot_exchanges_volume['bitstamp_vol_in_eth']\
                                          .astype('float64')
spot_exchanges_volume['okex_vol_in_eth'] = spot_exchanges_volume['okex_vol_in_eth']\
                                          .astype('float64')
spot_exchanges_volume['bitfinex_vol_in_eth'] = spot_exchanges_volume['bitfinex_vol_in_eth']\
                                          .astype('float64')
spot_exchanges_volume['huobi_vol_in_eth'] = spot_exchanges_volume['huobi_vol_in_eth']\
                                          .astype('float64')
spot_exchanges_volume['gemini_vol_in_eth'] = spot_exchanges_volume['gemini_vol_in_eth']\
                                          .astype('float64')

# %%

## Export Finished Dataframes to Pickles, so we won't hit API rate limits in the Dash dashboard
eth_90d.to_pickle('eth_90d.pkl')
eth_gas_fee.to_pickle('eth_gas_fee.pkl')
eth_combined_data_final.to_pickle('eth_combined_data_final.pkl')
eth_defi_tvl.to_pickle('eth_defi_tvl.pkl')
eth_defi_tvl_top10.to_pickle('eth_defi_tvl_top10.pkl')
spot_exchanges_volume.to_pickle('spot_exchanges_volume.pkl')
