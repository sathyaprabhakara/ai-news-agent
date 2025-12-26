from typing import List, Dict, Optional
from .memory_store import store
import logging

logger = logging.getLogger(__name__)

KEYWORDS = [
    "ai",
    "openai",
    "gpt",
    "llm",
    "machine learning",
    "artificial intelligence",
]


def matches_keywords(article: Dict) -> bool:
    text = (article.get("title", "") + " " + article.get("summary", "")).lower()
    for k in KEYWORDS:
        if k in text:
            return True
    return False


def select_article(candidates: List[Dict]) -> Optional[Dict]:
    """Return a single best article that matches keywords and not in memory."""
    for art in candidates:
        url = art.get("link")
        if not url:
            continue
        if store.has_article(url):
            logger.info("Skipping seen article: %s", url)
            continue
        if not matches_keywords(art):
            logger.info("Skipping non-matching article: %s", url)
            continue
        return art
    return None
