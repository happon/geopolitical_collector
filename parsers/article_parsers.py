from bs4 import BeautifulSoup
import re

# Import tag filters
from . import tag_filters

def parse_newsweek(soup):
    """
    Parse Newsweek article HTML soup to extract text content and tags.
    """
    # Remove unwanted elements (scripts, ads, etc.)
    for tag in soup.find_all(tag_filters.UNWANTED_TAGS):
        tag.decompose()
    for selector in tag_filters.DOMAIN_FILTERS.get('newsweek.com', []):
        for element in soup.select(selector):
            element.decompose()
    # Find main article content container
    content_div = soup.find(attrs={"data-js": "article-body"}) or soup.find(attrs={"itemprop": "articleBody"})
    article_text = ""
    if content_div:
        # Get text content from paragraphs
        paragraphs = content_div.find_all('p')
        article_text = "\n\n".join(p.get_text().strip() for p in paragraphs)
    else:
        # Fallback: get text from all paragraphs on page
        article_text = "\n\n".join(p.get_text().strip() for p in soup.find_all('p'))
    # Extract tags from meta keywords or topic links
    tags = []
    meta = soup.find('meta', attrs={'name': 'keywords'})
    if meta:
        content = meta.get('content', '')
        if content:
            tags = [t.strip() for t in content.split(',') if t.strip()]
    # Also try to get tags from topic links on the page
    for a in soup.find_all('a', href=True):
        if '/topic/' in a['href'] or '/tag/' in a['href']:
            tag_text = a.get_text().strip()
            if tag_text and tag_text not in tags:
                tags.append(tag_text)
    return article_text, tags

def parse_thehackernews(soup):
    """
    Parse The Hacker News article HTML soup to extract text content and tags.
    """
    # Remove unwanted elements
    for tag in soup.find_all(tag_filters.UNWANTED_TAGS):
        tag.decompose()
    for selector in tag_filters.DOMAIN_FILTERS.get('thehackernews.com', []):
        for element in soup.select(selector):
            element.decompose()
    # Find main content container (post body)
    content_div = soup.find('div', attrs={'class': 'post-body'}) or soup.find('div', attrs={'itemprop': 'articleBody'})
    if not content_div:
        content_div = soup
    paragraphs = content_div.find_all(['p', 'blockquote'])
    article_text = "\n\n".join(el.get_text().strip() for el in paragraphs)
    # Extract tags from labels (categories) at bottom of the post
    tags = []
    for a in soup.find_all('a', href=True):
        if '/search/label/' in a['href']:
            tag_text = a.get_text().strip()
            if tag_text and tag_text not in tags:
                tags.append(tag_text)
    return article_text, tags

def parse_mandiant(item):
    """
    Parse Mandiant API item (JSON) to extract content and tags.
    """
    # Assuming item is a dict with keys like 'description', 'tags', etc.
    content = ""
    tags = []
    if isinstance(item, dict):
        # Combine fields as content (if description or summary exists)
        if 'description' in item:
            content = item['description']
        elif 'details' in item:
            content = item['details']
        elif 'summary' in item:
            content = item['summary']
        else:
            # If no obvious content field, combine all values to a string
            content = " ".join(str(v) for v in item.values() if isinstance(v, str))
        # Tags might be under 'tags' or 'labels' or similar
        if 'tags' in item and isinstance(item['tags'], list):
            tags = [str(t) for t in item['tags']]
        elif 'labels' in item and isinstance(item['labels'], list):
            tags = [str(t) for t in item['labels']]
        elif 'actors' in item and isinstance(item['actors'], list):
            tags = [str(a) for a in item['actors']]
    return content, tags

# Domain to parser function mapping
PARSERS = {
    'newsweek.com': parse_newsweek,
    'thehackernews.com': parse_thehackernews,
    'mandiant.com': parse_mandiant,
    'api.mandiant.com': parse_mandiant
}

def parse_article(domain, content):
    """
    Dispatch to the appropriate parser based on domain. Content can be HTML (string or soup) or data item.
    """
    # If content is a raw HTML string, parse it with BeautifulSoup
    soup = None
    if isinstance(content, str):
        soup = BeautifulSoup(content, 'html.parser')
    # If content is already a BeautifulSoup object
    elif hasattr(content, 'find'):
        soup = content
    # Determine domain key
    parser_func = None
    for key, func in PARSERS.items():
        if key in domain:
            parser_func = func
            break
    if parser_func is None:
        # Default behavior: if content is soup or HTML
        if soup:
            # Extract text from all paragraphs
            text = "\n".join(p.get_text().strip() for p in soup.find_all('p'))
            return text, []
        else:
            # If content is data
            return str(content), []
    if parser_func in (parse_newsweek, parse_thehackernews):
        # Ensure we have a BeautifulSoup for HTML parsers
        if not soup:
            soup = BeautifulSoup(content, 'html.parser')
        return parser_func(soup)
    elif parser_func is parse_mandiant:
        # For API data, content is expected as dict item
        return parser_func(content)
    else:
        # Fallback to calling parser directly
        return parser_func(content)
