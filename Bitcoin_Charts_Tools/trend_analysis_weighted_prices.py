### Script Overview: `trend_analysis_weighted_prices.py`

# This script will perform the following tasks:
# 1. Read the JSON data to extract weighted prices for Bitcoin across different currencies and time periods (24h, 7d, 30d).
# 2. Calculate the average weighted price for each currency over the specified time periods.
# 3. Plot these trends over time to visually represent Bitcoin's volatility.
# 4. Save the plots to disk, with titles that reflect the currency and time period analyzed.

### Python Script Skeleton
import json
import pandas as pd
import matplotlib.pyplot as plt
import os  # Import os module

def read_json_data(filename='bitcoin_data.json'):
    # Get the directory of the current script
    current_dir = os.path.dirname(__file__)
    # Construct the full path to the JSON file
    file_path = os.path.join(current_dir, filename)
    
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def prepare_weighted_price_data(data):
    weighted_prices = data['weighted_prices']
    weighted_prices.pop('timestamp', None)  # Remove 'timestamp' if present
    df_list = []
    for currency, prices in weighted_prices.items():
        if isinstance(prices, dict):  # Ensure prices is a dictionary before proceeding
            for period, price in prices.items():
                df_list.append([currency, period, float(price)])
    df = pd.DataFrame(df_list, columns=['Currency', 'Period', 'Weighted Price'])
    return df

def plot_weighted_prices(df):
    # Directory where plots will be saved
    save_dir = 'Bitcoin_Charts'
    # Ensure the directory exists
    os.makedirs(save_dir, exist_ok=True)  # Create the directory if it doesn't exist
    
    currencies = df['Currency'].unique()
    for currency in currencies:
        fig, ax = plt.subplots(figsize=(8, 5))
        currency_df = df[df['Currency'] == currency]
        periods = ['24h', '7d', '30d']
        prices = [currency_df[currency_df['Period'] == period]['Weighted Price'].values[0] for period in periods]
        
        ax.bar(periods, prices)
        ax.set_title(f'Bitcoin Weighted Prices for {currency}')
        ax.set_ylabel('Weighted Price')
        ax.set_xlabel('Time Period')
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        # Adjust file saving path to include the directory
        plt.savefig(os.path.join(save_dir, f'{currency}_weighted_prices.png'))
        plt.close()

def main():
    data = read_json_data()
    df = prepare_weighted_price_data(data)
    plot_weighted_prices(df)

if __name__ == '__main__':
    main()
