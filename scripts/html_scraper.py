import logging
import time
from selenium.webdriver.chrome.options import Options
from seleniumbase import SB
import undetected_chromedriver as uc

def fetch_html_content(url: str) -> str:
    """
    URL からレンダリング後の HTML を取得します。
    SeleniumBase の UC モードを優先し、Failover として undetected_chromedriver 単体にも対応。
    """

    # ▼ 方法①：SeleniumBase を使って CAPTCHA を可能な限り回避
    try:
        with SB(uc=True, incognito=True, xvfb=True) as sb:
            sb.uc_open_with_reconnect(url, reconnect_time=5)
            sb.uc_gui_click_captcha()  # CAPTCHA に遭遇した場合の自動クリック
            html = sb.get_page_source()
            return html
    except Exception as e:
        logging.warning(f"SeleniumBase UC fetch failed for {url}: {e}")

    # ▼ 方法②：undetected-chromedriver 単体モードでの取得（フォールバック）
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    try:
        driver = uc.Chrome(options=options)
    except Exception as e:
        logging.error(f"Failed to launch uc.Chrome for {url}: {e}")
        return ""

    html = ""
    try:
        driver.get(url)
        time.sleep(3)  # JS レンダリングのため待機
        html = driver.page_source
    except Exception as e:
        logging.error(f"Failed to load page {url} with uc.Chrome: {e}")
    finally:
        driver.quit()

    return html
