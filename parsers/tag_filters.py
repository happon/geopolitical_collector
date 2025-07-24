# geopolitical_collector/parsers/tag_filters.py

# 共通の不要タグ（全ドメイン共通）
UNWANTED_TAGS = ["script", "style", "aside", "noscript", "footer", "form", "nav"]

# ドメイン別の除去用 CSS セレクタ
DOMAIN_FILTERS = {
    "newsweek.com": [
        "div.article-body__bottom",     # 著者紹介などの定型フッター
        "div.bottom-cta",               # 下部のサブスク誘導
        "div.inline-newsletter",        # メール購読
        "div.newsletter-signup",        # メルマガ登録
        "div[class*='ad']",
        "div[class*='share']",
        "div[class*='footer']",
        "div[class*='disclaimer']",
        "div[class*='promotion']"
    ],
    "thehackernews.com": [
        "div.post-labels",
        "div.author-box",
        "div#disqus_thread",
        "div.post-footer",
        "div#related_posts",
        "footer",
        "aside",
        "nav",
    ],
}
