import yfinance as yf


class FundamentalAnalyser:
    """
    A class to analyze the financial fundamentals of a company using Yahoo Finance.

    Attributes:
        stock (yfinance.Ticker): An instance of the yfinance Ticker class for the given stock symbol.
    """

    def __init__(self, ticker: str):
        self.stock = yf.Ticker(ticker)

    def get_financial_summary(self) -> dict:
        """
        Fetches and returns a summary of key financial metrics for the company.

        Returns:
            dict: A dictionary containing key financial metrics such as ROE, EBITDA, margins, debt, etc.
        """
        info = self.stock.info
        return {
            "Company": info.get("shortName"),
            "ROE": info.get("returnOnEquity"),
            "EBITDA": info.get("ebitda"),
            "Gross Margin": info.get("grossMargins"),
            "Operating Margin": info.get("operatingMargins"),
            "Debt to Equity": info.get("debtToEquity"),
            "Current Ratio": info.get("currentRatio"),
            "Total Debt": info.get("totalDebt"),
            "Total Revenue": info.get("totalRevenue"),
        }
