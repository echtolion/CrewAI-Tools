import requests
import pandas as pd
import matplotlib.pyplot as plt

# Function to fetch weighted prices
def fetch_weighted_prices():
    url = "http://api.bitcoincharts.com/v1/weighted_prices.json"
    response = requests.get(url)
    data = response.json()
    # Prepare a more flexible structure to handle unexpected data formats
    prepared_data = {}
    for currency, values in data.items():
        if isinstance(values, dict):  # Ensure the values are indeed a dictionary
            prepared_data[currency] = values
        else:
            prepared_data[currency] = {'error': 'Data format unexpected'}
    return pd.DataFrame.from_dict(prepared_data, orient='index')


# Function to gather market data
def fetch_market_data():
    url = "http://api.bitcoincharts.com/v1/markets.json"
    response = requests.get(url)
    data = response.json()
    return pd.DataFrame(data)

# Function to access historical trades (example for one market)
def fetch_historical_trades(symbol="bitstampUSD"):
    url = f"http://api.bitcoincharts.com/v1/trades.csv?symbol={symbol}"
    df = pd.read_csv(url, names=['unixtime', 'price', 'amount'])
    return df

# Example usage
weighted_prices = fetch_weighted_prices()
market_data = fetch_market_data()
historical_trades = fetch_historical_trades()  # default example with bitstampUSD

# Simple visualization example
historical_trades.plot(x='unixtime', y='price', title='Historical Trades Price Movement')
plt.show()
