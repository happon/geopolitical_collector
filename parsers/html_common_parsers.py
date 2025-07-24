from bs4 import BeautifulSoup
from .tag_filters import UNWANTED_TAGS, DOMAIN_FILTERS

def clean_html(html: str, domain: str) -> BeautifulSoup:
    """
    HTML文字列を BeautifulSoup に変換し、不要タグや共有フィルタを適用して返す。
    """
    soup = BeautifulSoup(html, "html.parser")

    # 共通の不要タグ削除
    for tag in soup.find_all(UNWANTED_TAGS):
        tag.decompose()

    # ドメイン別不要要素削除
    for selector in DOMAIN_FILTERS.get(domain, []):
        for element in soup.select(selector):
            element.decompose()

    return soup
