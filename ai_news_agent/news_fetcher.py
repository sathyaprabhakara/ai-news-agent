import feedparser
from typing import List, Dict
from .config import cfg
import logging

logger = logging.getLogger(__name__)


def fetch_latest() -> List[Dict]:
    """Fetch latest articles from the configured Google News RSS feed.

    Returns list of dicts with keys: title, link, summary, published
    """
    url = cfg.RSS_URL
    logger.info("Fetching RSS feed: %s", url)
    feed = feedparser.parse(url)
    if not feed.entries:
        logger.warning("RSS feed returned no entries")
        return []

    articles = []
    for entry in feed.entries[: cfg.MAX_FETCH]:
        articles.append(
            {
                "title": entry.get("title", "") ,
                "link": entry.get("link", ""),
                "summary": entry.get("summary", entry.get("description", "")),
                "published": entry.get("published", ""),
            }
        )

    logger.info("Fetched %d articles", len(articles))
    return articles
