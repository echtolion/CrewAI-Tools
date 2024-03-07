import json
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta

def read_json_data(filename='bitcoin_data.json'):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, filename)
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def read_events_data(filename='significant_events.csv'):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, filename)
    return pd.read_csv(file_path, parse_dates=['date'])

def prepare_price_volume_data(data):
    # Assuming 'market_data' contains the price and volume data
    market_data = data['market_data']
    df = pd.DataFrame(market_data)
    df['date'] = pd.to_datetime(df['latest_trade'], unit='s').dt.date
    return df

def correlate_and_plot(data_df, events_df):
    plt.figure(figsize=(12, 8))
    
    # Plotting price or volume trend
    # For simplicity, let's assume we're plotting closing prices; adjust as needed
    data_df.groupby('date')['close'].mean().plot(label='Daily Closing Price')
    
    # Marking significant events
    for _, row in events_df.iterrows():
        plt.axvline(x=row['date'], color='r', linestyle='--', alpha=0.5)
        plt.text(row['date'], plt.ylim()[1], row['event'], rotation=90, verticalalignment='top')
    
    plt.title('Bitcoin Prices and Significant Events')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    
    save_dir = 'Bitcoin_Charts'
    os.makedirs(save_dir, exist_ok=True)
    plt.savefig(os.path.join(save_dir, 'event_price_correlation.png'))
    plt.close()

def main():
    bitcoin_data = read_json_data()
    events_data = read_events_data()
    price_volume_df = prepare_price_volume_data(bitcoin_data)
    correlate_and_plot(price_volume_df, events_data)

if __name__ == '__main__':
    main()
