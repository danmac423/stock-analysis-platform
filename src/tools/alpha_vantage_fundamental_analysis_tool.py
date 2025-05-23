import json

from crewai.tools import tool

from src.services.alpha_vantage_fundamental_analyser import AlphaVantageFundamentalAnalyser


@tool
def analyse_fundamentals(stock_symbol: str, n_quarters: int = 4) -> str:
    """
    Fetches and analyses fundamental data for a given stock symbol using Alpha Vantage.
    Data includes earnings, revenue, cash flow, and balance sheet information.

    Args:
        stock_symbol (str): The stock ticker symbol to analyze.
        n_quarters (int): The number of quarters of data to fetch. Default is 4.

    Returns:
        str: A JSON string containing the fetched fundamental data.
    """
    analyser = AlphaVantageFundamentalAnalyser(stock_symbol)
    data = analyser.get_fundamental_data(n_quarters=n_quarters)

    return json.dumps(data, indent=2)
