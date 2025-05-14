import json

from crewai.tools import tool

from services.company_news_fetcher import CompanyNewsFetcher

news_fetcher = CompanyNewsFetcher()


@tool
def fetch_company_news(stock_symbol: str, days: int = 1) -> str:
    """
    Fetches recent company news for the given stock symbol and summarizes it.

    Args:
        stock_symbol (str): e.g. AAPL, TSLA
        days (int): How many days back to look

    Returns:
        str: A summary of recent company news
    """
    news = news_fetcher.fetch_news(stock_symbol, days)
    return json.dumps(news, indent=2)
