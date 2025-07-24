import pytest
from parsers.html_parsers.newsweek import extract_newsweek
from parsers.html_common_parsers import clean_html
from parsers.base_parser import ParsedArticle

def test_extract_newsweek_with_sample_html():
    sample_html = """
    <html><head><title>Test Newsweek</title></head>
    <body>
      <div data-js="article-body">
        <p>First paragraph.</p>
        <p>Second paragraph.</p>
      </div>
      <meta name="keywords" content="tag1, tag2, tag3">
    </body></html>
    """
    meta = {
        "name": "Newsweek",
        "url": "https://www.newsweek.com/test",
        "category": "PoliticalEconomy",
        "published": "2025-07-10T12:00:00Z"
    }
    parsed: ParsedArticle = extract_newsweek(sample_html, meta)
    assert isinstance(parsed, ParsedArticle)
    assert "First paragraph." in parsed.article
    assert parsed.title == "Test Newsweek"
    assert "tag1" in parsed.tags

def test_clean_html_removes_script_tags():
    raw_html = "<html><body><script>alert('x');</script><p>OK</p></body></html>"
    soup = clean_html(raw_html, "newsweek.com")
    assert soup.find("script") is None
    assert soup.find("p").get_text(strip=True) == "OK"
