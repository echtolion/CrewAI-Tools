from langchain.tools import tool

@tool
def fetch_historical_trades_tool(symbol: str = "bitstampUSD") -> pd.DataFrame:
    """
    Accesses historical trades for a given market symbol from the Bitcoin Charts API.
    The symbol parameter defaults to 'bitstampUSD'.
    Returns a pandas DataFrame with columns for unixtime, price, and amount.
    """
    url = f"http://api.bitcoincharts.com/v1/trades.csv?symbol={symbol}"
    df = pd.read_csv(url, names=['unixtime', 'price', 'amount'])
    return df
