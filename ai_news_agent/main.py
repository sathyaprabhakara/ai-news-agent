import logging
import sys
from .news_fetcher import fetch_latest
from .news_filter import select_article
from .summarizer import generate_tweet
from .twitter_client import client as twitter_client
from .emailer import send_email
from .memory_store import store
from .config import cfg

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger("ai_news_agent")


def run_once():
    logger.info("Agent started")

    articles = fetch_latest()
    if not articles:
        logger.info("No articles fetched; exiting")
        return

    article = select_article(articles)
    if not article:
        logger.info("No suitable new article found; exiting")
        return

    tweet = generate_tweet(article)
    if not tweet:
        logger.error("Failed to generate tweet; exiting")
        return

    # Validate length and exact 3 lines
    if len(tweet) > 280 or tweet.count("\n") != 2:
        logger.error("Tweet failed post-validation; not posting")
        return

    try:
        tweet_id = twitter_client.post_tweet(tweet)
    except Exception as e:
        logger.exception("Error posting to Twitter: %s", e)
        tweet_id = None

    # Email the tweet text + article link (shortened)
    subject = "Daily AI News Tweet"
    link = article.get("link", "")
    # Truncate very long URLs
    if len(link) > 80:
        link = link[:77] + "..."
    body = tweet + "\n\nSource: " + link
    email_ok = send_email(subject, body)

    # Store in memory to avoid duplicates
    store.save_entry(article.get("link", ""), tweet, tweet_id)

    logger.info("Run complete. tweet_id=%s email_sent=%s", tweet_id, email_ok)


if __name__ == "__main__":
    try:
        run_once()
    except Exception:
        logger.exception("Unhandled exception in agent")
        sys.exit(1)
