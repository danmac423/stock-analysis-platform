from services.reddit.reddit_sentiment import RedditSentimentAnalyzer
from crewai.tools import tool

analyzer = RedditSentimentAnalyzer()

@tool
def reddit_analyser(subreddits: list, stock: str, post_limit=50, days=30) -> dict:
    """
    Analyzes Reddit sentiment for a given stock across multiple subreddits.

    Args:
        subreddits (list): A list of subreddit names (e.g., ['stocks', 'investing']).
        stock (str): The stock ticker or keyword to search for (e.g., 'AAPL').
        post_limit (int): Maximum number of posts to analyze per subreddit.
        days (int): Time window (in days) to look back for Reddit posts.

    Returns:
        dict: A count of 'positive', 'neutral', and 'negative' sentiment results.
    """
    return analyzer.analyze(subreddits, stock, post_limit, days)