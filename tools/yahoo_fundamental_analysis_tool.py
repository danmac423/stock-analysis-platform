import json

from crewai.tools import tool

from services.yahoo_fundamental_analyser import FundamentalAnalyser


@tool
def analyse_fundamentals(stock_symbol: str) -> str:
    """
    Extracts and interprets financial metrics (ROE, EBITDA, margins, debt) for a company.
    """
    analyser = FundamentalAnalyser(stock_symbol)
    data = analyser.get_financial_summary()

    return json.dumps(data, indent=2)
