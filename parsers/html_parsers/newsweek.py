import re
from ..base_parser import ParsedArticle
from ..html_common_parsers import clean_html

def extract_newsweek(html: str, meta: dict) -> ParsedArticle:
    soup = clean_html(html, "newsweek.com")

    # 本文抽出
    content_div = soup.find(attrs={"data-js": "article-body"}) or soup.find(attrs={"itemprop": "articleBody"})
    paragraphs = content_div.find_all("p") if content_div else soup.find_all("p")
    paragraph_texts = [p.get_text(strip=True) for p in paragraphs]

    author = None
    author_patterns = [
        r"([A-Z][a-z]+(?: [A-Z][a-z]+)+) is a Newsweek",  # 2語以上の名前対応
        r"([A-Z][a-z]+(?: [A-Z][a-z]+)+) is a .*?Newsweek .*?Reporter",
        r"([A-Z][a-z]+(?: [A-Z][a-z]+)+) is a freelance .*? for Newsweek",
    ]

    cleaned_paragraphs = []
    for para in paragraph_texts:
        matched = False
        for pattern in author_patterns:
            match = re.match(pattern, para)
            if match:
                author = match.group(1)
                matched = True
                break
        if not matched:
            cleaned_paragraphs.append(para)

    # 不要な冒頭定型文の除去
    remove_prefixes = [
        "This is a modal window.",
        "Newsweek AI is in beta.",
        "🎙️ Voice is AI-generated.",
        "Inconsistencies may occur."
    ]
    article = "\n\n".join(cleaned_paragraphs)
    for prefix in remove_prefixes:
        if article.startswith(prefix):
            article = article.split(prefix, 1)[-1].strip()

    # 不要な末尾の誘導リンク削除（例: "More MLB:")
    article = re.split(r"\n+More [A-Z]{2,}:", article)[0].strip()

    # タイトル
    og_title = soup.find("meta", property="og:title")
    title = og_title["content"].strip() if og_title and og_title.get("content") else (
        soup.title.string.strip() if soup.title else "No Title"
    )

    # 投稿日
    published_meta = soup.find("meta", property="article:published_time")
    published = published_meta["content"] if published_meta and published_meta.get("content") else meta.get("published", "")

    # タグ
    meta_tag = soup.find("meta", {"name": "keywords"})
    tags = meta_tag["content"].split(",") if meta_tag and meta_tag.get("content") else []

    return ParsedArticle(
        source=meta["name"],
        category=meta["category"],
        title=title,
        link=meta["url"],
        published=published,
        article=article,
        tags=[t.strip() for t in tags if t.strip()],
        author=author
    )
