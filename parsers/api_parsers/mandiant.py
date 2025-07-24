from ..base_parser import ParsedArticle
from ..api_common_parsers import extract_basic_api_fields

def extract_mandiant(data: dict, meta: dict) -> ParsedArticle:
    title, link, published, content, tags = extract_basic_api_fields(data)

    return ParsedArticle(
        source=meta["name"],
        category=meta["category"],
        title=title,
        link=link or meta["url"],
        published=published,
        article=content.strip(),
        tags=tags
    )
