import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import finnhub

load_dotenv()


class CompanyNewsFetcher:
    def __init__(self):
        self.api_key = os.getenv("FINNHUB_API_KEY")
        self.client = finnhub.Client(api_key=self.api_key)
        self.endpoint = "https://finnhub.io/api/v1/company-news"

    def fetch_news(self, symbol: str, days: int = 7) -> list:
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
