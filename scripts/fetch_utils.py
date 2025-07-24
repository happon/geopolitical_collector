import json
import logging
import os
import time
import re
from datetime import datetime, timedelta
import requests

# ディレクトリ設定
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
DATA_DIR = os.path.join(BASE_DIR, "data", "raw_articles")
os.makedirs(DATA_DIR, exist_ok=True)

def is_recent(entry, hours=24):
    try:
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            # RSSフィードの時刻をUTC基準で取得
            entry_time = datetime.fromtimestamp(time.mktime(entry.published_parsed))
            now = datetime.utcnow()
            delta = now - entry_time

            logging.debug(f"[DEBUG] entry_time={entry_time}, now={now}, delta={delta}")

            return delta.total_seconds() < hours * 3600
    except Exception as e:
        logging.warning(f"[WARNING] is_recent failed: {e}")
    return False

def sanitize_filename(title: str) -> str:
    # タイトルを安全なファイル名に変換
    filename = title.strip()
    filename = filename.replace(" ", "_")
    filename = re.sub(r'[\\/*?:"<>|]', "", filename)  # Windows等で使えない文字を除去
    filename = re.sub(r"_{2,}", "_", filename)        # アンダースコア連続を1つに
    return filename[:150]                             # 念のため最大150文字に制限

def save_article(article_data: dict):
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    title_part = sanitize_filename(article_data.get("title", "untitled"))
    filename = f"{timestamp}_{title_part}.json"
    filepath = os.path.join(DATA_DIR, filename)

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(article_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logging.error(f"Failed to save article: {e}")

def fetch_api_data(api_url: str) -> list:
    headers = {"Accept": "application/json"}
    try:
        resp = requests.get(api_url, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, dict):
                for key in ["data", "items", "results", "articles", "entries"]:
                    if key in data and isinstance(data[key], list):
                        return data[key]
                return [data]
            elif isinstance(data, list):
                return data
        else:
            logging.error(f"API status {resp.status_code}: {resp.text}")
    except Exception as e:
        logging.error(f"API request failed: {e}")
    return []
