import os
from crewai import Agent, Task, Crew, LLM
from tools.reddit_sentiment_analyzer_tool import reddit_analyser
from tools.stock_news_tool import company_news_summary
from tools.yahoo_fundamental_analysis_tool import analyze_fundamentals
from dotenv import load_dotenv


# This script is just to verify implementation of agents, and it's output
# Reformat will be needed

load_dotenv()

my_llm = LLM(
    model="gemini/gemini-2.0-flash",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.2
)

stock_sentiment_agent = Agent(
    role='Senior Stock Market Researcher',
    goal='Analyze recent Reddit sentiment about a given stock',
    backstory="With a Ph.D.in Financial Economics and 15 years of experience in equity research, you're known for your meticulous data collection and insightful analysis.",
    llm=my_llm,
    tools=[reddit_analyser, company_news_summary],
    verbose=True
)

fundamental_agent = Agent(
    role="Equity Research Analyst",
    goal="Assess a company's financial health using quantitative indicators.",
    backstory="You're a CFA-certified analyst with a deep understanding of corporate finance and balance sheets.",
    tools=[analyze_fundamentals],
    llm=my_llm,
    verbose=True
)

summary_agent = Agent(
    role="Investment Strategy Advisor",
    goal="Summarize sentiment and fundamentals into a single investment perspective.",
    backstory="You specialize in synthesizing market data into strategic insights for investors.",
    llm=my_llm,
    verbose=True
)

task1 = Task(
    description=(
        "Conduct research on {stock_symbol}. Your analysis should include:\n"
        "1. Current stock price and historical performance (5 years).\n"
        "2. Key financial metrics (P/E, EPS growth, revenue growth, margins).\n"
        "3. Recent news and press releases (1 month).\n"
        "4. Analyst ratings and price targets (min 3 analysts).\n"
        "5. Reddit sentiment analysis (100 posts).\n"
        "6. Major institutional holders and recent changes.\n"
        "7. Competitive landscape and {stock_symbol}'s market share.\n"
        "Use reputable financial websites for data."
    ),
    expected_output='A detailed 150-word research report with data sources and brief analysis.',
    agent=stock_sentiment_agent
)

task2 = Task(
    description="Evaluate the financial condition of AAPL using ROE, EBITDA, margins, and debt ratios.",
    expected_output="A concise 150-word analysis of AAPL's financial strength based on key financial indicators.",
    agent=fundamental_agent
)

task3 = Task(
    description=(
        "Summarize the following information about {stock_symbol} into a final investment insight:\n"
        "1. Sentiment and market news analysis (task 1)\n"
        "2. Fundamental financial analysis (task 2)\n"
        "Provide a concise, clear investment recommendation (bullish, bearish, or neutral), with rationale."
    ),
    expected_output="A 100-word strategic investment summary combining both sentiment and fundamentals.",
    agent=summary_agent,
    async_dependencies=[task1, task2]
)

crew = Crew(
    agents=[stock_sentiment_agent],
    tasks=[task1, task2, task3],
    cache=True,
    verbose=True
)

result = crew.kickoff(inputs={'stock_symbol': 'AAPL'})
print("\n=== Agent Output ===")
print(result)