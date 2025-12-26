import os
from dataclasses import dataclass
from typing import Optional


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    val = os.getenv(name, default)
    if val is None:
        return None
    return val


@dataclass
class Config:
    OPENAI_API_KEY: Optional[str] = _env("OPENAI_API_KEY")
    OPENAI_MODEL: str = _env("OPENAI_MODEL") or "gpt-4o-mini"

    TWITTER_API_KEY: Optional[str] = _env("TWITTER_API_KEY")
    TWITTER_API_SECRET: Optional[str] = _env("TWITTER_API_SECRET")
    TWITTER_ACCESS_TOKEN: Optional[str] = _env("TWITTER_ACCESS_TOKEN")
    TWITTER_ACCESS_SECRET: Optional[str] = _env("TWITTER_ACCESS_SECRET")

    EMAIL_FROM: Optional[str] = _env("EMAIL_FROM")
    EMAIL_PASSWORD: Optional[str] = _env("EMAIL_PASSWORD")
    EMAIL_TO: Optional[str] = _env("EMAIL_TO")

    RSS_URL: str = _env("RSS_URL") or "https://news.google.com/rss/search?q=artificial+intelligence"
    MAX_FETCH: int = int(_env("MAX_FETCH") or 5)

    MEMORY_DB: str = _env("MEMORY_DB") or "memory.db"

    DRY_RUN: bool = (_env("DRY_RUN") or "false").lower() in ("1", "true", "yes")


cfg = Config()
