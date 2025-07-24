import logging
from urllib.parse import urlparse

from .rss_collector import get_feed_entries
from .html_scraper import fetch_html_content
from .fetch_utils import save_article, is_recent, fetch_api_data
from ..parsers import parse_article
from geopolitical_collector.parsers.rss_common_parsers import extract_basic_rss_fields

def handle_source(source: dict, test_mode: bool = False) -> int:
    saved_count = 0
    per_source_limit = 1 if test_mode else float('inf')

    url = source.get("url")
    domain = source.get("domain", "")
    name = source.get("name", "Unnamed")
    category = source.get("category", "Uncategorized")

    if is_rss_source(url):
        entries = get_feed_entries(url)
        for entry in entries:
            logging.debug(f"[DEBUG] Entry title: {getattr(entry, 'title', '')}")
            logging.debug(f"[DEBUG] Entry published: {getattr(entry, 'published', '')}")
            logging.debug(f"[DEBUG] Entry published_parsed: {getattr(entry, 'published_parsed', None)}")

            if not is_recent(entry):
                logging.info(f"[INFO] Skipped (not recent): {getattr(entry, 'link', '')}")
                continue

            title, link, published = extract_basic_rss_fields(entry)
            meta = {
                "name": name,
                "url": link,
                "category": category,
                "published": published,
                "title": title
            }

            html = fetch_html_content(link)
            if not html:
                logging.warning(f"[WARNING] Empty HTML for {link}")
                continue
            logging.info(f"[DEBUG] HTML length={len(html)} for {link}")

            parsed = parse_article(domain, html, meta)
            if not parsed:
                logging.warning(f"[WARNING] parse_article returned None for {link}")
                continue

            logging.info(f"[DEBUG] Parsed {domain}: title={parsed.title!r}, author={getattr(parsed, 'author', '')!r}, len={len(parsed.article)}")
            save_article(parsed.to_dict())

            saved_count += 1
            if saved_count >= per_source_limit:
                break

    elif is_api_source(url, domain):
        items = fetch_api_data(url)
        for item in items:
            parsed = parse_article(domain, item, {
                "name": name,
                "url": url,
                "category": category
            })
            if not parsed:
                logging.warning(f"[WARNING] parse_article returned None for API item")
                continue
            if not parsed.published or is_recent(parsed.published):
                save_article(parsed.to_dict())
                saved_count += 1
                if saved_count >= per_source_limit:
                    break

    else:
        html = fetch_html_content(url)
        if not html:
            logging.warning(f"[WARNING] Empty HTML for direct HTML source {url}")
            return 0
        parsed = parse_article(domain, html, {
            "name": name,
            "url": url,
            "category": category
        })
        if not parsed:
            logging.warning(f"[WARNING] parse_article returned None for {url}")
            return 0
        save_article(parsed.to_dict())
        saved_count += 1

    return saved_count

def is_rss_source(url: str) -> bool:
    return url.endswith(".xml") or "rss" in url or "feeds." in url

def is_api_source(url: str, domain: str) -> bool:
    return "api." in domain or "/api" in url
