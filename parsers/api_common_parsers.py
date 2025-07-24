def extract_basic_api_fields(data: dict):
    """
    APIレスポンス（dict）から共通的に使えそうなフィールドを抽出。
    """
    title = data.get("title") or data.get("name") or "No Title"
    link = data.get("link") or ""
    published = data.get("published") or data.get("date") or ""
    summary = data.get("summary") or data.get("description") or data.get("details") or ""

    tags = []
    for key in ["tags", "labels", "actors"]:
        if key in data and isinstance(data[key], list):
            tags = data[key]
            break

    return title, link, published, summary, tags
