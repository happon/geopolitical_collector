import feedparser

def extract_basic_rss_fields(entry):
    """
    feedparser の entry オブジェクトから title, link, published を抽出する共通処理。
    """
    title = getattr(entry, 'title', 'No Title')
    link = getattr(entry, 'link', '')
    published = getattr(entry, 'published', '')
    return title, link, published
