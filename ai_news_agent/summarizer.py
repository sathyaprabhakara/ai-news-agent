from openai import OpenAI
from .config import cfg
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def _build_prompt(article: dict) -> str:
    tmpl = (
        "You are a concise assistant. Create a short, neutral, informative tweet about the article provided."
        "Follow these strict rules:\n"
        "- Exactly 3 short lines separated by single newlines\n"
        "- Max 280 characters total (including newlines)\n"
        "- No emojis, no hashtags, no markdown\n"
        "- Neutral, informative tone\n"
        "- Each line must add value and be short\n"
        "Provide only the tweet text, nothing else.\n\n"
        "Article Title:\n{title}\n\n"
        "Article Summary:\n{summary}\n\n"
        "Article Link: {link}\n"
    )
    return tmpl.format(title=article.get("title", ""), summary=article.get("summary", ""), link=article.get("link", ""))


def generate_tweet(article: dict, max_retries: int = 2) -> Optional[str]:
    # Dry-run: return a deterministic, compliant tweet without calling OpenAI
    if cfg.DRY_RUN:
        title = (article.get("title") or "")[:80]
        line1 = f"{title}"
        line2 = f"Source: {article.get('link','')[:60]}"
        line3 = "More details in the linked article."
        tweet = "\n".join([line1, line2, line3])
        if len(tweet) <= 280 and tweet.count("\n") == 2:
            logger.info("Dry-run tweet generated")
            return tweet
        # fallthrough to normal path if something unexpected
    if not cfg.OPENAI_API_KEY:
        logger.error("OPENAI_API_KEY not set")
        return None
    prompt = _build_prompt(article)

    client = OpenAI(api_key=cfg.OPENAI_API_KEY)

    for attempt in range(max_retries + 1):
        try:
            logger.info("Requesting tweet from OpenAI (attempt %d)", attempt + 1)
            resp = client.chat.completions.create(
                model=cfg.OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=200,
            )
            text = resp.choices[0].message.content.strip()
            # Post-process: normalize lines and attempt to produce exactly 3 non-empty short lines
            raw_lines = [l.strip() for l in text.splitlines() if l.strip()]
            if len(raw_lines) >= 3:
                candidate = "\n".join(raw_lines[:3])
                if len(candidate) <= 280:
                    return candidate
                # if candidate too long, try truncating the last line
                last = raw_lines[2]
                allowed = 280 - (len(raw_lines[0]) + len(raw_lines[1]) + 2)
                if allowed > 0:
                    truncated_last = last[:allowed]
                    candidate = "\n".join([raw_lines[0], raw_lines[1], truncated_last])
                    if len(candidate) <= 280:
                        return candidate
                logger.warning("Generated tweet too long after trimming (%d). Retrying...", len(candidate))

            # If fewer than 3 non-empty lines, or we couldn't make a compliant tweet, retry
            logger.warning("Generated tweet does not have 3 usable lines (got %d). Retrying...", len(raw_lines))
            continue
        except Exception as e:
            logger.exception("OpenAI request failed: %s", e)
    logger.error("Failed to generate a compliant tweet after %d attempts", max_retries + 1)
    return None
