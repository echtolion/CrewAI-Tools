from langchain.tools import tool

@tool
def fetch_market_data_tool() -> pd.DataFrame:
    """
    Gathers market data from the Bitcoin Charts API.
    Returns a pandas DataFrame with the market data.
    """
    url = "http://api.bitcoincharts.com/v1/markets.json"
    response = requests.get(url)
    data = response.json()
    return pd.DataFrame(data)
