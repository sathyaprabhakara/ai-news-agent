import logging
import tweepy
from .config import cfg
from typing import Optional

logger = logging.getLogger(__name__)


class TwitterClient:
    def __init__(self):
        self.dry_run = cfg.DRY_RUN
        if not all([cfg.TWITTER_API_KEY, cfg.TWITTER_API_SECRET, cfg.TWITTER_ACCESS_TOKEN, cfg.TWITTER_ACCESS_SECRET]):
            logger.warning("Twitter credentials are not fully set; client will be disabled.")
            self.client = None
            return

        self.client = tweepy.Client(
            consumer_key=cfg.TWITTER_API_KEY,
            consumer_secret=cfg.TWITTER_API_SECRET,
            access_token=cfg.TWITTER_ACCESS_TOKEN,
            access_token_secret=cfg.TWITTER_ACCESS_SECRET,
            wait_on_rate_limit=True,
        )

    def post_tweet(self, text: str) -> Optional[str]:
        if len(text) > 280:
            raise ValueError("Tweet exceeds 280 characters")
        if self.dry_run or self.client is None:
            logger.info("Dry-run or client missing — not posting tweet. Text:\n%s", text)
            return None

        try:
            resp = self.client.create_tweet(text=text)
            tweet_id = None
            if resp and hasattr(resp, "data") and resp.data:
                tweet_id = resp.data.get("id")
            logger.info("Tweet posted: id=%s", tweet_id)
            return tweet_id
        except Exception as e:
            logger.exception("Failed to post tweet: %s", e)
            return None


client = TwitterClient()
