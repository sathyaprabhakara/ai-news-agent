import sqlite3
import time
from typing import Optional
import logging
from .config import cfg

logger = logging.getLogger(__name__)


class MemoryStore:
    def __init__(self, path: Optional[str] = None):
        self.path = path or cfg.MEMORY_DB
        self._conn = sqlite3.connect(self.path, check_same_thread=False)
        self._ensure_table()

    def _ensure_table(self):
        cur = self._conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS tweets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE,
                tweet_text TEXT,
                tweet_id TEXT,
                ts INTEGER
            )
            """
        )
        self._conn.commit()

    def has_article(self, url: str) -> bool:
        cur = self._conn.cursor()
        cur.execute("SELECT 1 FROM tweets WHERE url = ? LIMIT 1", (url,))
        found = cur.fetchone() is not None
        return found

    def save_entry(self, url: str, tweet_text: str, tweet_id: Optional[str]):
        cur = self._conn.cursor()
        cur.execute(
            "INSERT OR IGNORE INTO tweets (url, tweet_text, tweet_id, ts) VALUES (?, ?, ?, ?)",
            (url, tweet_text, tweet_id or "", int(time.time())),
        )
        self._conn.commit()


store = MemoryStore()
