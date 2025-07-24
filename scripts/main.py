import argparse
import logging
from .controller import run_collection

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", help="Run in test mode (1 article per source)")
    args = parser.parse_args()

    logging.basicConfig(
        filename="geopolitical_collector/logs/scraper.log",
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

    run_collection(test_mode=args.test)
