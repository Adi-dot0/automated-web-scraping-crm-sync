# Selenium handler - for websites that load data with JavaScript.
#
# The demo site used in this project (books.toscrape.com) is plain HTML,
# so the main scraper uses requests + BeautifulSoup. This module is the
# ready pattern from the project specification for dynamic pages:
# it opens the page in a real (headless) browser, waits for the content
# to load, and returns the rendered HTML for the same parser.
#
# Requires: pip install selenium  (and a Chrome/Chromium browser)

import time


def fetch_with_selenium(url, wait_seconds=3):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        time.sleep(wait_seconds)  # let JavaScript finish loading
        return driver.page_source
    finally:
        driver.quit()
