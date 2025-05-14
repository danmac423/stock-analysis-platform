from services.reddit.reddit_client import RedditClient
from services.reddit.sentiment_analyzer import SentimentAnalyzer

class RedditSentimentAnalyzer:
    def __init__(self):
        self.reddit_client = RedditClient()
        self.sentiment_analyzer = SentimentAnalyzer()

    def analyze(self, subreddits: list, stock: str, post_limit=50, days=30):
        sentiment_counts = {'neutral': 0, 'negative': 0, 'positive': 0}
        for subreddit in subreddits:
            posts = self.reddit_client.get_posts(subreddit, stock, post_limit, days)
            for post in posts:
                text = f"{post.title}\n{post.selftext}"
                sentiment = self.sentiment_analyzer.analyze(text)
                sentiment_counts[sentiment] += 1
        return sentiment_counts