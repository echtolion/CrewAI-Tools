import requests
import pandas as pd
import matplotlib.pyplot as plt
import json
import os

# Ensure the values are not None or replace them with a default value
def clean_values(values):
    return {k: (v if v is not None else "N/A") for k, v in values.items()}

def fetch_weighted_prices():
    url = "http://api.bitcoincharts.com/v1/weighted_prices.json"
    response = requests.get(url)
    data = response.json()
    prepared_data = {currency: clean_values(values) if isinstance(values, dict) else {'error': 'Data format unexpected'} for currency, values in data.items()}
    return pd.DataFrame.from_dict(prepared_data, orient='index')

def fetch_market_data():
    url = "http://api.bitcoincharts.com/v1/markets.json"
    response = requests.get(url)
    market_data = [clean_values(item) for item in response.json()]
    return pd.DataFrame(market_data)

def fetch_historical_trades(symbol="bitstampUSD"):
    url = f"http://api.bitcoincharts.com/v1/trades.csv?symbol={symbol}"
    df = pd.read_csv(url, names=['unixtime', 'price', 'amount'])
    return df

def fetch_and_save_data():
    weighted_prices_data = fetch_weighted_prices().to_dict()
    market_data = fetch_market_data().to_dict(orient='records')
    historical_trades = fetch_historical_trades(symbol="bitstampUSD").to_dict(orient='records')

    combined_data = {
        'weighted_prices': weighted_prices_data,
        'market_data': market_data,
        'historical_trades': historical_trades
    }
    
    # Create a directory in the current script's root directory and save the JSON there
    save_dir = os.path.join(os.getcwd(), 'Bitcoin_Data')
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, 'complete_bitcoin_data.json')
    
    with open(save_path, 'w') as f:
        json.dump(combined_data, f, indent=4)

def plot_historical_trades():
    historical_trades = fetch_historical_trades()
    historical_trades.plot(x='unixtime', y='price', title='Historical Trades Price Movement')
    plt.show()

if __name__ == "__main__":
    fetch_and_save_data()
    plot_historical_trades()
