import os
from dotenv import load_dotenv
import praw
from datetime import datetime, timedelta, timezone

load_dotenv()

class RedditClient:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT'),
        )

    def get_posts(self, subreddit: str, query: str, post_limit=50, days=30):
        sub = self.reddit.subreddit(subreddit)
        start_date = datetime.now(timezone.utc) - timedelta(days=days)
        posts = []

        for post in sub.search(query, sort='new', time_filter='all', limit=post_limit):
            post_date = datetime.fromtimestamp(post.created_utc, tz=timezone.utc)
            if post_date >= start_date:
                posts.append(post)
        return posts