import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class CompanyNewsFetcher:
    def __init__(self):
        self.api_key = os.getenv("FINNHUB_API_KEY")
        self.endpoint = "https://finnhub.io/api/v1/company-news"

    def fetch_news(self, symbol: str, days: int = 7) -> list:
        to_date = datetime.now().strftime('%Y-%m-%d')
        from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

        params = {
            "symbol": symbol.upper(),
            "from": from_date,
            "to": to_date,
            "token": self.api_key
        }

        response = requests.get(self.endpoint, params=params)

        if response.status_code != 200:
            raise Exception(f"Finnhub API error: {response.status_code} - {response.text}")

        articles = response.json()
        return [
            {
                "headline": article["headline"],
                "summary": article.get("summary", ""),
                "source": article["source"],
                "url": article["url"],
                "datetime": datetime.fromtimestamp(article["datetime"]).strftime("%Y-%m-%d %H:%M")
            }
            for article in articles
        ]