from crewai import LLM
from crewai.tools import tool
from services.yahoo_fundamental_analyzer import FundamentalAnalyzer
from dotenv import load_dotenv
import os

load_dotenv()
llm = LLM(model="gemini/gemini-2.0-flash", api_key=os.getenv("GEMINI_API_KEY"))

@tool
def analyze_fundamentals(stock_symbol: str) -> str:
    """
    Extracts and interprets financial metrics (ROE, EBITDA, margins, debt) for a company.
    """
    analyzer = FundamentalAnalyzer(stock_symbol)
    data = analyzer.get_financial_summary()

    metrics = "\n".join([f"{k}: {v}" for k, v in data.items()])
    prompt = (
        f"Based on the following financial data for {stock_symbol}, assess the company's financial health:\n\n"
        f"{metrics}\n\nGive a clear, concise assessment with explanation."
    )

    return llm.call(prompt)
