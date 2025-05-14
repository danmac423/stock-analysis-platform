import os
from datetime import datetime, timedelta

import finnhub
from dotenv import load_dotenv

load_dotenv()


class CompanyNewsFetcher:
    """
    A class to fetch company news using the Finnhub API.

    Attributes:
        client (finnhub.Client): An instance of the Finnhub API client.
    """

    def __init__(self):
        self.client = finnhub.Client(api_key=os.getenv("FINNHUB_API_KEY"))

    def fetch_news(self, symbol: str, days: int = 7) -> list:
        """
        Fetches recent company news for the given stock symbol.
        Args:
            symbol (str): The stock symbol (e.g., AAPL, TSLA).
            days (int): How many days back to look for news.
        Returns:
            list: A list of dictionaries containing news articles with their headlines, summaries, sources, URLs, and timestamps.
        """
        to_date = datetime.now().strftime("%Y-%m-%d")
        from_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

        articles = self.client.company_news(symbol, _from=from_date, to=to_date)

        return [
            {
                "headline": article["headline"],
                "summary": article.get("summary", ""),
                "source": article["source"],
                "url": article["url"],
                "datetime": datetime.fromtimestamp(article["datetime"]).strftime(
                    "%Y-%m-%d %H:%M"
                ),
            }
            for article in articles
        ]
