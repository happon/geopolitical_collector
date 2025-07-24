import feedparser
import logging
from geopolitical_collector.scripts.fetch_utils import is_recent

def get_feed_entries(url: str) -> list:
    feed = feedparser.parse(url)
    entries = []

    for entry in feed.entries:
        if is_recent(entry):
            logging.debug(f"[DEBUG] [DEBUG] Entry title: {entry.title}")
            logging.debug(f"[DEBUG] [DEBUG] Entry published: {entry.get('published', '')}")
            logging.debug(f"[DEBUG] [DEBUG] Entry published_parsed: {entry.get('published_parsed')}")
            logging.debug(f"[DEBUG] [DEBUG] Entry author: {entry.get('author', 'N/A')}")

            entries.append(entry)

    logging.info(f"Found {len(entries)} recent entries in feed: {url}")
    return entries

def extract_basic_rss_fields(entry) -> tuple:
    title = entry.get("title", "")
    link = entry.get("link", "")
    published = entry.get("published", "")
    return title, link, published
