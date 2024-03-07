import json
import pandas as pd
import matplotlib.pyplot as plt
import os

def read_json_data(filename='bitcoin_data.json'):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, filename)
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def prepare_bid_ask_data(data):
    market_data = data['market_data']
    df = pd.DataFrame(market_data)
    # Calculate the bid-ask spread
    df['spread'] = df['ask'] - df['bid']
    return df[df['spread'].notnull()]  # Filter out entries without both bid and ask data

def analyze_and_plot_spreads(df):
    plt.figure(figsize=(10, 6))
    # Plot the distribution of spreads
    df['spread'].plot(kind='hist', bins=50, alpha=0.7)
    plt.title('Distribution of Bid-Ask Spreads Across Markets')
    plt.xlabel('Spread')
    plt.ylabel('Frequency')
    
    # Highlighting mean and median spread
    plt.axvline(df['spread'].mean(), color='r', linestyle='dashed', linewidth=1, label='Mean Spread')
    plt.axvline(df['spread'].median(), color='g', linestyle='dotted', linewidth=1, label='Median Spread')
    plt.legend()

    save_dir = 'Bitcoin_Charts'
    os.makedirs(save_dir, exist_ok=True)
    plt.savefig(os.path.join(save_dir, 'bid_ask_spread_distribution.png'))
    plt.close()

def main():
    data = read_json_data()
    df = prepare_bid_ask_data(data)
    analyze_and_plot_spreads(df)

if __name__ == '__main__':
    main()
