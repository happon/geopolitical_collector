from geopolitical_collector.parsers.base_parser import ParsedArticle
from geopolitical_collector.parsers.html_common_parsers import clean_html
from geopolitical_collector.scripts.html_scraper import fetch_html_content
import re

def extract_thehackernews(content, meta: dict) -> ParsedArticle:
    """
    content は次のどちらか：
      • RSS entry object → entry.link を使って fetch_html_content を呼ぶ
      • HTML文字列 → そのまま解析
    """
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

    # 最後に "（The story is developing...）" のような末尾文を削除
    if "The story is developing" in text:
        text = text.split("The story is developing")[0].strip()

    # タイトル
    title_tag = soup.find("meta", property="og:title")
    title = title_tag["content"].strip() if title_tag and title_tag.get("content") else meta.get("title", meta.get("name", ""))

    # 投稿日
    pub_tag = soup.find("meta", property="article:published_time")
    published = pub_tag["content"] if pub_tag and pub_tag.get("content") else meta.get("published", "")

    # タグ抽出
    tags = []
    for a in soup.find_all("a", href=True):
        if "/search/label/" in a["href"]:
            tag = a.get_text(strip=True)
            if tag and tag not in tags:
                tags.append(tag)

    # 著者抽出（<span class="author"> から抽出、先頭のアイコン文字や日付を除去）
    author = None
    author_spans = soup.find_all("span", class_="author")
    for span in author_spans:
        raw = span.get_text(strip=True)
        clean = re.sub(r"^[^\w]*", "", raw)
        parts = clean.split()

        # 日付形式の箇所ならスキップ
        if len(parts) >= 3 and parts[0].isalpha() and parts[1].strip(',').isdigit() and parts[2].isdigit():
            continue
        # 人名らしければ著者として採用
        if len(parts) >= 2 and all(p[0].isupper() for p in parts[:2]):
            author = " ".join(parts)
            break

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
