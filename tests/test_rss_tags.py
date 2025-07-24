import pytest
from parsers.rss_common_parsers import extract_basic_rss_fields
import feedparser

@pytest.fixture
def dummy_entry():
    return type("E", (), {
        "title": "Title",
        "link": "http://example.com",
        "published": "Wed, 10 Jul 2025 12:00:00 GMT"
    })()

def test_extract_basic_rss_fields(dummy_entry):
    title, link, published = extract_basic_rss_fields(dummy_entry)
    assert title == "Title"
    assert link.endswith("example.com")
    assert "2025" in published
