import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import requests
from crewai import Agent
from langchain.tools import tool

class BitcoinTools():
    
    @tool("Clean Values Tool")
    def clean_values(self, values):
        """Cleans a given dictionary by ensuring that none of its values are None, replacing any None values with 'N/A'."""
        return {k: (v if v is not None else "N/A") for k, v in values.items()}

    @tool("Fetch Weighted Prices Tool")
    def fetch_weighted_prices(self):
        """Fetches weighted Bitcoin prices from an API and formats the data into a pandas DataFrame."""
        url = "http://api.bitcoincharts.com/v1/weighted_prices.json"
        response = requests.get(url)
        data = response.json()
        prepared_data = {currency: self.clean_values(values) if isinstance(values, dict) else {'error': 'Data format unexpected'} for currency, values in data.items()}
        return pd.DataFrame.from_dict(prepared_data, orient='index')

    @tool("Fetch Market Data Tool")
    def fetch_market_data(self):
        """Retrieves market data for Bitcoin from an API and presents it as a pandas DataFrame."""
        url = "http://api.bitcoincharts.com/v1/markets.json"
        response = requests.get(url)
        market_data = [self.clean_values(item) for item in response.json()]
        return pd.DataFrame(market_data)

    @tool("Fetch Historical Trades Tool")
    def fetch_historical_trades(self, symbol="bitstampUSD"):
        """Gathers historical trade data for a specified Bitcoin market symbol."""
        url = f"http://api.bitcoincharts.com/v1/trades.csv?symbol={symbol}"
        df = pd.read_csv(url, names=['unixtime', 'price', 'amount'])
        return df

    @tool("Fetch And Save Data Tool")
    def fetch_and_save_data(self, symbol="bitstampUSD"):
        """Combines fetching weighted prices, market data, and historical trades, then saves the combined data into a JSON file."""
        weighted_prices_data = self.fetch_weighted_prices().to_dict()
        market_data = self.fetch_market_data().to_dict(orient='records')
        historical_trades = self.fetch_historical_trades(symbol=symbol).to_dict(orient='records')

        combined_data = {
            'weighted_prices': weighted_prices_data,
            'market_data': market_data,
            'historical_trades': historical_trades
        }
        
        save_dir = os.path.join(os.getcwd(), 'Bitcoin_Data')
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, 'complete_bitcoin_data.json')
        
        with open(save_path, 'w') as f:
            json.dump(combined_data, f, indent=4)
        return save_path

    @tool("Plot Historical Trades Tool")
    def plot_historical_trades(self):
        """Plots the price movement of historical Bitcoin trades over time."""
        historical_trades = self.fetch_historical_trades()
        historical_trades.plot(x='unixtime', y='price', title='Historical Trades Price Movement')
        plt.show()

    @tool("BidAskSpreadAnalysisTool")
    def bid_ask_spread_analysis(self):
        """
        Analyzes bid-ask spreads for Bitcoin across different currencies from the market data.
        Returns a DataFrame with currencies and their respective bid-ask spreads.
        """
        # Assuming market_data is a DataFrame obtained from the fetch_market_data tool
        market_data = self.fetch_market_data()
        
        # Ensure market_data contains 'bid' and 'ask' columns
        if 'bid' in market_data.columns and 'ask' in market_data.columns:
            # Calculate bid-ask spread
            market_data['bid_ask_spread'] = market_data['ask'] - market_data['bid']
            
            # Filter relevant columns
            analysis_result = market_data[['currency', 'bid', 'ask', 'bid_ask_spread']]
            
            return analysis_result.sort_values(by='bid_ask_spread', ascending=False)
        else:
            return pd.DataFrame(columns=['currency', 'bid', 'ask', 'bid_ask_spread'], data=[['Data Unavailable', 'N/A', 'N/A', 'N/A']])
        
    @tool("Market Activity Volume Analysis Tool")
    def market_activity_volume_analysis(self, symbol="bitstampUSD"):
        """Analyzes and plots the volume of trades over time for a specified Bitcoin market symbol."""
        # Fetch historical trades for the specified symbol
        url = f"http://api.bitcoincharts.com/v1/trades.csv?symbol={symbol}"
        df = pd.read_csv(url, names=['unixtime', 'price', 'amount'])

        # Convert unixtime to datetime for plotting
        df['datetime'] = pd.to_datetime(df['unixtime'], unit='s')

        # Plotting the trade volume over time
        plt.figure(figsize=(10, 6))
        plt.plot(df['datetime'], df['amount'], label='Trade Volume')
        plt.title(f'Trade Volume Over Time for {symbol}')
        plt.xlabel('Time')
        plt.ylabel('Volume')
        plt.legend()
        plt.show()

    @tool("Trend Analysis Weighted Prices Tool")
    def analyze_weighted_prices_trend(self, start_date, end_date):
        """Analyzes trends in weighted Bitcoin prices over a specified period."""
        # Fetch weighted prices data for the specified period
        weighted_prices_data = self.fetch_weighted_prices() # Assuming this method exists and fetches historical data

        # Filter data for the specified period
        start_timestamp = datetime.strptime(start_date, '%Y-%m-%d').timestamp()
        end_timestamp = datetime.strptime(end_date, '%Y-%m-%d').timestamp()
        filtered_data = weighted_prices_data[(weighted_prices_data['timestamp'] >= start_timestamp) & (weighted_prices_data['timestamp'] <= end_timestamp)]

        # Calculate trend indicators (e.g., moving average)
        filtered_data['SMA_30'] = filtered_data['price'].rolling(window=30).mean()

        # Plot the data and moving average
        plt.figure(figsize=(12,6))
        plt.plot(filtered_data['timestamp'], filtered_data['price'], label='Weighted Prices')
        plt.plot(filtered_data['timestamp'], filtered_data['SMA_30'], label='30-day SMA', color='orange')
        plt.xlabel('Date')
        plt.ylabel('Weighted Price')
        plt.title('Trend Analysis of Weighted Bitcoin Prices')
        plt.legend()
        plt.show()

        # Summarize the trend
        trend_summary = "Trend analysis completed. Review the plot for trend insights."
        return trend_summary
        
    @tool("24-Hour Historical Volatility Calculator")
    def calculate_24_hour_historical_volatility(self):
        """Calculates the 24-hour historical volatility of Bitcoin prices."""
        weighted_prices = self.fetch_weighted_prices()  # Fetch weighted prices data

        time_period = '24h'
        if time_period in weighted_prices:
            prices_data = weighted_prices[time_period]['USD']  # Focus on USD prices

            if isinstance(prices_data, (int, float)):
                return {"error": "Insufficient data for volatility analysis."}
            
            prices_df = pd.DataFrame([prices_data], columns=['price'])
            prices_df['log_returns'] = np.log(prices_df['price'] / prices_df['price'].shift(1))
            
            volatility = prices_df['log_returns'].std() * np.sqrt(365)  # Annualized volatility
            
            return {"24_hour_volatility": volatility}
        else:
            return {"error": "24-hour data not found."}
        
    @tool("7-Day Historical Volatility Calculator")
    def calculate_7_day_historical_volatility(self):
        """Calculates the 7-day historical volatility of Bitcoin prices."""
        weighted_prices = self.fetch_weighted_prices()  # Fetch weighted prices data

        time_period = '7d'
        if time_period in weighted_prices:
            prices_data = weighted_prices[time_period]['USD']  # Focus on USD prices

            if isinstance(prices_data, (int, float)):
                return {"error": "Insufficient data for volatility analysis."}
            
            prices_df = pd.DataFrame([prices_data], columns=['price'])
            prices_df['log_returns'] = np.log(prices_df['price'] / prices_df['price'].shift(1))
            
            volatility = prices_df['log_returns'].std() * np.sqrt(365)  # Annualized volatility
            
            return {"7_day_volatility": volatility}
        else:
            return {"error": "7-day data not found."}

    @tool("30-Day Historical Volatility Calculator")
    def calculate_30_day_historical_volatility(self):
        """Calculates the 30-day historical volatility of Bitcoin prices."""
        # Fetch weighted prices data, assuming such a method exists and retrieves data including for the past 30 days
        weighted_prices = self.fetch_weighted_prices()

        # Specific focus on the 30d time period
        time_period = '30d'
        
        if time_period in weighted_prices:
            # Example focuses on USD prices; adjust as necessary for your dataset
            prices_data = weighted_prices[time_period]['USD']
            
            # Ensure data is in the correct format, convert to DataFrame for analysis
            if isinstance(prices_data, (int, float)):
                return {"error": "Insufficient data for volatility analysis."}
            
            prices_df = pd.DataFrame(prices_data)
            prices_df['log_returns'] = np.log(prices_df / prices_df.shift(1))
            
            # Calculate the standard deviation of logarithmic returns (annualized)
            volatility = prices_df['log_returns'].std() * np.sqrt(365)
            
            return {"30_day_volatility": volatility}
        else:
            return {"error": "30-day data not found."}