import feedparser
import logging
import time
from datetime import datetime, timezone, timedelta

def get_feed_entries(feed_url):
    feed = feedparser.parse(feed_url)
    if feed.bozo:
        logging.error(f"Failed to parse feed: {feed_url}")
        return []

    entries = []
    now = datetime.now(timezone.utc)

    for entry in feed.entries:
        try:
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                pub_dt = datetime.fromtimestamp(time.mktime(entry.published_parsed), tz=timezone.utc)
            elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                pub_dt = datetime.fromtimestamp(time.mktime(entry.updated_parsed), tz=timezone.utc)
            else:
                pub_dt = now

            if now - pub_dt < timedelta(days=2):
                entries.append(entry)
        except Exception as e:
            logging.warning(f"Failed to parse entry timestamp: {e}")
            entries.append(entry)

    logging.info(f"Found {len(entries)} recent entries in feed: {feed_url}")
    return entries
