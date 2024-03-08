from langchain.tools import tool

@tool
def fetch_weighted_prices_tool() -> pd.DataFrame:
    """
    Fetches weighted prices for various currencies from the Bitcoin Charts API.
    Returns a pandas DataFrame indexed by currency, with columns for different price metrics.
    """
    url = "http://api.bitcoincharts.com/v1/weighted_prices.json"
    response = requests.get(url)
    data = response.json()
    # Prepare a flexible structure to handle unexpected data formats
    prepared_data = {}
    for currency, values in data.items():
        if isinstance(values, dict):  # Ensure values are a dictionary
            prepared_data[currency] = values
        else:
            prepared_data[currency] = {'error': 'Data format unexpected'}
    return pd.DataFrame.from_dict(prepared_data, orient='index')
