import pytest
from parsers.api_parsers.mandiant import extract_mandiant
from parsers.base_parser import ParsedArticle

def test_extract_mandiant_minimal():
    data = {
        "title": "Threat Detected",
        "link": "http://api.example.com/1",
        "published": "2025-07-11T08:00:00Z",
        "description": "Details of threat",
        "tags": ["tagA", "tagB"]
    }
    meta = {
        "name": "Mandiant",
        "url": "https://api.mandiant.com/v1/threats",
        "category": "ThreatIntel"
    }
    parsed: ParsedArticle = extract_mandiant(data, meta)
    assert parsed.title == "Threat Detected"
    assert "Details of threat" in parsed.article
    assert "tagB" in parsed.tags
