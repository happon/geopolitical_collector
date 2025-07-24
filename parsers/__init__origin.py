from .html_parsers.newsweek import extract_newsweek
from .html_parsers.thehackernews import extract_thehackernews
from .html_parsers.bleepingcomputer import extract_bleepingcomputer
from .api_parsers.mandiant import extract_mandiant
import logging

PARSER_MAP = {
    "newsweek.com": extract_newsweek,
    "thehackernews.com": extract_thehackernews,
    "bleepingcomputer.com": extract_bleepingcomputer,
    "mandiant.com": extract_mandiant,
    "api.mandiant.com": extract_mandiant
}

def parse_article(domain: str, content, meta: dict):
    logging.info(f"[DEBUG] parse_article called: domain={domain}, title={meta.get('title')}")
    for key in PARSER_MAP:
        if key in domain:
            return PARSER_MAP[key](content, meta)
    raise ValueError(f"No parser registered for domain: {domain}")
