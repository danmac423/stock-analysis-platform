import yfinance as yf

class FundamentalAnalyzer:
    def __init__(self, ticker: str):
        self.stock = yf.Ticker(ticker)

    def get_financial_summary(self):
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
