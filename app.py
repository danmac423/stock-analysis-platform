import streamlit as st
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import yfinance as yf
from agents import StockAnalysisCrew
from markdown_it import MarkdownIt

def format_markdown(text):
    md = MarkdownIt()
    tokens = md.parse(text)
    formatted = ""
    for token in tokens:
        if token.type == "paragraph_open":
            formatted += "\n\n"
        formatted += token.content
    return formatted.strip()

def escape_markdown_specials(text: str) -> str:
    text = text.replace('$', r'\$')
    return text

def load_stock_data(symbol: str, period: str):
    return yf.download(symbol, period=period, auto_adjust=True, progress=False)


class StockAnalysisApp:
    def __init__(self):

        st.set_page_config("Stock Investment Report", layout="wide")
        st.title("📈 Stock Investment Analysis Platform")
        self._render_sidebar()

    def _render_sidebar(self):
        st.sidebar.header("Configuration")
        self.stock_symbol = st.sidebar.text_input("Enter stock symbol", "").upper()
        self.api_key      = st.sidebar.text_input("Enter Gemini API key", type="password")
        self.period       = st.sidebar.selectbox("Select time period",
                                                 ['1mo', '3mo', '6mo', '1y', '2y', '5y'],
                                                 index=2)

        if st.sidebar.button("Generate report"):
            if not (self.stock_symbol and self.api_key):
                st.sidebar.warning("Please enter both a stock symbol and an API key.")
                return
            self.run_analysis()

    def plot_stock_chart(self, stock_data):
        stock_data = stock_data.xs(self.stock_symbol, axis=1, level=1)
        fig = make_subplots(rows=1, cols=1, shared_xaxes=True)

        fig.add_trace(
            go.Candlestick(
                x=stock_data.index,
                open=stock_data["Open"],
                high=stock_data["High"],
                low=stock_data["Low"],
                close=stock_data["Close"],
                name="Price"
            ),
            row=1, col=1
        )

        fig.update_layout(
            title="Stock Price",
            height=600,
            xaxis_rangeslider_visible=False,
            showlegend=False
        )

        fig.update_xaxes(
            rangeselector=dict(
                buttons=[
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=3, label="3m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ]
            ),
            rangeslider=dict(visible=False),
            type="date"
        )

        return fig

    def run_analysis(self):
        with st.spinner("Running multi-agent analysis…"):
            result = StockAnalysisCrew(self.stock_symbol, self.api_key).run()

        markdown = format_markdown(str(result))
        cleaned = escape_markdown_specials(markdown)
        with st.expander("Investment report", expanded=True):
            st.markdown(cleaned, unsafe_allow_html=True)

        fig = self.plot_stock_chart(yf.download(self.stock_symbol, period=self.period))
        st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    StockAnalysisApp()
