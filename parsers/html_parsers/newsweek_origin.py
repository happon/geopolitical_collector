from ..base_parser import ParsedArticle
from ..html_common_parsers import clean_html

def extract_newsweek(html: str, meta: dict) -> ParsedArticle:
    soup = clean_html(html, "newsweek.com")

    # 本文抽出
    content_div = soup.find(attrs={"data-js": "article-body"}) or soup.find(attrs={"itemprop": "articleBody"})
    paragraphs = content_div.find_all("p") if content_div else soup.find_all("p")
    text = "\n\n".join(p.get_text(strip=True) for p in paragraphs)

    # 不要な冒頭の定型文を削除
    remove_prefixes = [
        "This is a modal window.",
        "Newsweek AI is in beta.",
        "🎙️ Voice is AI-generated.",
        "Inconsistencies may occur."
    ]
    for prefix in remove_prefixes:
        if prefix in text:
            text = text.split(prefix, 1)[-1].strip()

    # 不要な末尾の定型文を削除
    remove_suffix_triggers = [
        "Zach Pressnell is a Newsweek contributor",
        "You can get in touch with",
        "Tyler Everett is a longtime",
        "Newsletters in your inbox",
        "Company",
        "Terms of Use",
        "© 2025 NEWSWEEK"
    ]
    for trigger in remove_suffix_triggers:
        if trigger in text:
            text = text.split(trigger, 1)[0].strip()

    # タイトル抽出
    og_title = soup.find("meta", property="og:title")
    title = og_title["content"].strip() if og_title and og_title.get("content") else (
        soup.title.string.strip() if soup.title else "No Title"
    )

    # 著者取得
    author_meta = soup.find("meta", {"name": "author"}) or soup.find("meta", property="article:author")
    author = author_meta["content"].strip() if author_meta and author_meta.get("content") else None

    # 投稿日の抽出
    published_meta = soup.find("meta", property="article:published_time")
    published = published_meta["content"] if published_meta and published_meta.get("content") else meta.get("published", "")

    # タグ取得
    meta_tag = soup.find("meta", {"name": "keywords"})
    tags = meta_tag["content"].split(",") if meta_tag and meta_tag.get("content") else []

    return ParsedArticle(
        source=meta["name"],
        category=meta["category"],
        title=title,
        link=meta["url"],
        published=published,
        article=text,
        tags=[t.strip() for t in tags if t.strip()],
        author=author
    )
