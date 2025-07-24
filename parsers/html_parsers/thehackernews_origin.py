from geopolitical_collector.parsers.base_parser import ParsedArticle
from geopolitical_collector.parsers.html_common_parsers import clean_html
from geopolitical_collector.scripts.html_scraper import fetch_html_content

def extract_thehackernews(content, meta: dict) -> ParsedArticle:
    """
    content は次のどちらか：
      • RSS entry object → entry.link を使って fetch_html_content を呼ぶ
      • HTML文字列 → そのまま解析
    """

    # RSSの entry オブジェクトか判定（hasattr で代用）
    if hasattr(content, 'link'):
        url = content.link
        html = fetch_html_content(url)
    else:
        html = content
        url = meta.get("url", "")

    soup = clean_html(html, "thehackernews.com")

    # 本文抽出
    content_div = soup.find("div", class_="post-body") or soup.find("div", itemprop="articleBody")
    paragraphs = content_div.find_all(["p", "blockquote"]) if content_div else soup.find_all("p")
    text = "\n\n".join(p.get_text(strip=True) for p in paragraphs)

    # タイトル抽出（HTMLから再取得）
    title_tag = soup.find("meta", property="og:title")
    title = title_tag["content"].strip() if title_tag and title_tag.get("content") else meta.get("title", meta.get("name", ""))

    # 著者抽出
    author_meta = soup.find("meta", {"name": "author"})
    author = author_meta["content"].strip() if author_meta else None

    # 投稿日抽出（HTML内metaタグ）
    pub_tag = soup.find("meta", property="article:published_time")
    published = pub_tag["content"] if pub_tag and pub_tag.get("content") else meta.get("published", "")

    # タグ抽出（HTML構造に合わせて補完）
    tags = []
    for a in soup.find_all("a", href=True):
        if "/search/label/" in a["href"]:
            tag = a.get_text(strip=True)
            if tag and tag not in tags:
                tags.append(tag)

    return ParsedArticle(
        source=meta["name"],
        category=meta["category"],
        title=title,
        link=url,
        published=published,
        article=text.strip(),
        tags=tags,
        author=author
    )
