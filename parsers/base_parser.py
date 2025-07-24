class ParsedArticle:
    def __init__(self, source, category, title, link, published, article, tags, author=None):
        self.source = source
        self.category = category
        self.title = title
        self.link = link
        self.published = published
        self.article = article
        self.tags = tags or []
        self.author = author

    def to_dict(self):
        return {
            "source": self.source,
            "category": self.category,
            "title": self.title,
            "link": self.link,
            "published": self.published,
            "article": self.article,
            "tags": self.tags,
            "author": self.author
        }
