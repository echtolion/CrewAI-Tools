import json
import pandas as pd
import matplotlib.pyplot as plt
import os

def read_json_data(filename='bitcoin_data.json'):
    # Assuming the function is adjusted to find the file in the current script's directory
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, filename)
    
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def prepare_market_activity_data(data):
    market_data = data['market_data']
    df = pd.DataFrame(market_data)
    # Convert 'latest_trade' to a readable date format (assuming it's a UNIX timestamp)
    df['date'] = pd.to_datetime(df['latest_trade'], unit='s')
    return df

def analyze_and_plot_volume(df):
    # Group data by date and sum up the volume for each day
    volume_by_date = df.groupby(df['date'].dt.date)['volume'].sum().reset_index()
    
    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(volume_by_date['date'], volume_by_date['volume'], marker='o', linestyle='-')
    plt.title('Daily Bitcoin Trading Volume')
    plt.xlabel('Date')
    plt.ylabel('Volume')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Ensure the directory exists
    save_dir = 'Bitcoin_Charts'
    os.makedirs(save_dir, exist_ok=True)
    plt.savefig(os.path.join(save_dir, 'daily_trading_volume.png'))
    plt.close()

def main():
    data = read_json_data()
    df = prepare_market_activity_data(data)
    analyze_and_plot_volume(df)

if __name__ == '__main__':
    main()
