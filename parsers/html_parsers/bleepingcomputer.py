import re
from geopolitical_collector.parsers.base_parser import ParsedArticle
from geopolitical_collector.parsers.html_common_parsers import clean_html
from geopolitical_collector.scripts.html_scraper import fetch_html_content

def extract_bleepingcomputer(content, meta: dict) -> ParsedArticle:
    if hasattr(content, "link"):
        url = content.link
        html = fetch_html_content(url)
    else:
        html = content
        url = meta.get("url", "")

    soup = clean_html(html, "bleepingcomputer.com")

    # 本文抽出
    content_div = soup.find("div", class_="articleBody")
    paragraphs = content_div.find_all("p") if content_div else soup.find_all("p")
    text = "\n\n".join(p.get_text(strip=True) for p in paragraphs)

    # タイトル
    title_tag = soup.find("meta", property="og:title")
    title = title_tag["content"].strip() if title_tag and title_tag.get("content") else meta.get("title", "")

    # 投稿日
    published_tag = soup.find("meta", property="article:published_time")
    published = published_tag["content"].strip() if published_tag and published_tag.get("content") else meta.get("published", "")

    # 著者
    author = meta.get("author") or None
    if not author:
        author_tag = soup.find("meta", attrs={"name": "author"})
        author = author_tag["content"].strip() if author_tag and author_tag.get("content") else None

    # タグ（HTML上部カテゴリ or 記事内リンクから抽出）
    tags = []
    tag_links = soup.select("a[href*='/news/']")
    for a in tag_links:
        tag_text = a.get_text(strip=True)
        if tag_text and tag_text.lower() not in tags:
            tags.append(tag_text)

    return ParsedArticle(
        source=meta.get("name", "BleepingComputer"),
        category=meta.get("category", "Cybersecurity"),
        title=title,
        link=url,
        published=published,
        article=text.strip(),
        tags=tags,
        author=author
    )
