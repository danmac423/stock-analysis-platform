from crewai import LLM
from crewai.tools import tool
from services.company_news_fetcher import CompanyNewsFetcher
import os

news_fetcher = CompanyNewsFetcher()
llm = LLM(model="gemini/gemini-2.0-flash", api_key=os.getenv("GEMINI_API_KEY"))

@tool
def company_news_summary(stock_symbol: str, days: int = 7) -> str:
    """
    Fetches recent company news for the given stock symbol and summarizes it.

    Args:
        stock_symbol (str): e.g. AAPL, TSLA
        days (int): How many days back to look

    Returns:
        str: A summary of recent company news
    """
    articles = news_fetcher.fetch_news(stock_symbol, days)

    if not articles:
        return "No recent news found."

    text = "\n\n".join([
        f"{a['headline']} ({a['datetime']})\nSource: {a['source']}\nSummary: {a['summary'] or '[No summary]'}\nURL: {a['url']}"
        for a in articles
    ])

    prompt = (
        f"Summarize the following news headlines about {stock_symbol} from the past {days} days:\n\n{text}\n\nSummary:"
    )

    return llm.call(prompt)
