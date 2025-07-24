from geopolitical_collector.parsers.html_parsers.newsweek import extract_newsweek
from geopolitical_collector.parsers.html_parsers.thehackernews import extract_thehackernews
from geopolitical_collector.parsers.html_parsers.bleepingcomputer import extract_bleepingcomputer

domain_dispatch = {
    "newsweek.com": extract_newsweek,
    "thehackernews.com": extract_thehackernews,
    "bleepingcomputer.com": extract_bleepingcomputer,
}

def parse_article(domain, html_or_entry, meta):
    parser = domain_dispatch.get(domain)
    if not parser:
        raise ValueError(f"No parser found for domain: {domain}")
    return parser(html_or_entry, meta)
