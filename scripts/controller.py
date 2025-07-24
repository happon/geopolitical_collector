import json
import logging
from pathlib import Path

from .source_handler import handle_source

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / 'config' / 'sources.json'

def run_collection(test_mode=False):
    """
    sources.json に定義された全ソースを順に処理する。
    """
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            sources = json.load(f)
    except Exception as e:
        logging.error(f"Failed to load sources.json: {e}")
        return

    logging.info(f"Starting collection ({'TEST' if test_mode else 'FULL'} mode)")
    total_saved = 0

    for source in sources:
        try:
            logging.info(f"Processing: {source.get('name')} ({source.get('url')})")
            saved_count = handle_source(source, test_mode=test_mode)
            total_saved += saved_count
        except Exception as e:
            logging.error(f"Error processing source {source.get('name')}: {e}", exc_info=True)

    logging.info(f"Finished collection. Total articles saved: {total_saved}")
