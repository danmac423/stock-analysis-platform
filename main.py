import os
from crewai import Agent, Task, Crew, LLM
from tools.reddit_sentiment_analyzer import reddit_analyser
from dotenv import load_dotenv

from tools.web_search_tool import web_search

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
    tools=[reddit_analyser, web_search],
    verbose=True
)

task = Task(
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

crew = Crew(
    agents=[stock_sentiment_agent],
    tasks=[task],
    cache=True
)
result = crew.kickoff(inputs={'stock_symbol': 'AAPL'})
print("\n=== Agent Output ===")
print(result)