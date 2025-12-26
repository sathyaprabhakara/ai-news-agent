# AI News Agent

This agent fetches the latest AI-related news, generates a concise 3-line tweet using OpenAI, posts it to Twitter (X), and emails the tweet. It stores posted articles locally to avoid duplicates.

**Files**
- `main.py`: Entrypoint orchestrating the workflow
- `config.py`: Environment-driven configuration
- `news_fetcher.py`: RSS fetcher (Google News)
- `news_filter.py`: Keyword filter and selection
- `summarizer.py`: OpenAI-based tweet generator
- `twitter_client.py`: Tweepy wrapper for posting
- `emailer.py`: SMTP email sender
- `memory_store.py`: SQLite memory for deduplication
- `requirements.txt`: Python dependencies

**Environment variables** (required)
- `OPENAI_API_KEY`
- `TWITTER_API_KEY`
- `TWITTER_API_SECRET`
- `TWITTER_ACCESS_TOKEN`
- `TWITTER_ACCESS_SECRET`
- `EMAIL_FROM` (Gmail address)
- `EMAIL_PASSWORD` (app password recommended)
- `EMAIL_TO`

Optional:
- `DRY_RUN` = `true` to avoid posting to Twitter (default: false)
- `RSS_URL` to override the default Google News query
- `MAX_FETCH` (defaults to 5)
- `MEMORY_DB` (defaults to `memory.db`)
- `OPENAI_MODEL` (defaults to `gpt-4o-mini`)


## Quickstart
1. Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r ai_news_agent/requirements.txt
```

2. Export environment variables (example):

```bash
export OPENAI_API_KEY=sk-...
export TWITTER_API_KEY=...
export TWITTER_API_SECRET=...
export TWITTER_ACCESS_TOKEN=...
export TWITTER_ACCESS_SECRET=...
export EMAIL_FROM=you@example.com
export EMAIL_PASSWORD=your_smtp_password
export EMAIL_TO=recipient@example.com
```

3. Run once:

```bash
python -m ai_news_agent.main
# or
python ai_news_agent/main.py
```

Use `DRY_RUN=true` to test without posting to Twitter.


## Scheduling

Cron (daily at 08:00):

```cron
0 8 * * * cd /path/to/repo && /path/to/venv/bin/python /path/to/repo/ai_news_agent/main.py >> /path/to/repo/ai_news_agent/agent.log 2>&1
```

GitHub Actions (daily): create `.github/workflows/daily.yml`:

```yaml
name: Daily AI Tweet
on:
  schedule:
    - cron: '0 8 * * *'
jobs:
  run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install deps
        run: |
          python -m pip install --upgrade pip
          pip install -r ai_news_agent/requirements.txt
      - name: Run agent
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          TWITTER_API_KEY: ${{ secrets.TWITTER_API_KEY }}
          TWITTER_API_SECRET: ${{ secrets.TWITTER_API_SECRET }}
          TWITTER_ACCESS_TOKEN: ${{ secrets.TWITTER_ACCESS_TOKEN }}
          TWITTER_ACCESS_SECRET: ${{ secrets.TWITTER_ACCESS_SECRET }}
          EMAIL_FROM: ${{ secrets.EMAIL_FROM }}
          EMAIL_PASSWORD: ${{ secrets.EMAIL_PASSWORD }}
          EMAIL_TO: ${{ secrets.EMAIL_TO }}
        run: |
          python ai_news_agent/main.py
```


## Notes
- Use an app-specific password for Gmail and enable SMTP access.
- The agent stores posted article URLs in `memory.db` to prevent duplicates.
- Errors are logged; the agent exits gracefully when no valid article is found.
